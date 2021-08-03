## [Setup linux](../../ubuntu/docs/setup_linux.md)
## [Setup docker](../../ubuntu/docs/setup_docker.md)

## create network workbench
```bash
docker network create workbench \
  --subnet 10.1.1.0/24
```

## create postgress
```bash
docker run -d \
  $(echo "$DOCKER_RUN_OPTS") \
  -h postgresql \
  -e POSTGRES_USER='root' \
  -e POSTGRES_PASSWORD='root' \
  -e POSTGRES_DB='dev' \
  -v postgresql-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --name postgresql \
  --network workbench \
  docker.io/library/postgres:12.6-alpine

sudo $(which hostess) add postgresql 127.0.0.1
```

## Criando base para ambari
docker exec -it postgresql psql --username=root dev -c "CREATE DATABASE ambari;"
docker exec -it postgresql psql --username=root ambari -c "CREATE USER ambaridba WITH PASSWORD 'ambaripwd';"
docker exec -it postgresql psql --username=root ambari -c "GRANT ALL PRIVILEGES ON DATABASE ambari TO ambaridba;"
docker exec -it postgresql psql --username=root ambari -c "CREATE SCHEMA ambari AUTHORIZATION ambaridba;"
docker exec -it postgresql psql --username=root ambari -c "ALTER SCHEMA ambari OWNER TO ambaridba;"
docker exec -it postgresql psql --username=root ambari -c "ALTER ROLE ambaridba SET search_path to 'ambari', 'public';"

## Criando usuario para ranger
```bash
docker exec -it postgresql psql --username=root dev -c "CREATE DATABASE ranger;" 
docker exec -it postgresql psql --username=root ranger -c "CREATE USER rangerdba WITH PASSWORD 'rangerpwd';"
docker exec -it postgresql psql --username=root ranger -c "GRANT ALL PRIVILEGES ON DATABASE ranger TO rangerdba;"
```


```bash
docker exec -it postgresql psql --username=root dev -c "CREATE DATABASE hive;" 
docker exec -it postgresql psql --username=root ranger -c "CREATE USER hivedba WITH PASSWORD 'hivepwd';"
docker exec -it postgresql psql --username=root ranger -c "GRANT ALL PRIVILEGES ON DATABASE hive TO hivedba;"
```

```bash
docker exec -it postgresql psql --username=root dev -c "CREATE DATABASE druid;" 
docker exec -it postgresql psql --username=root ranger -c "CREATE USER druiddba WITH PASSWORD 'druidpwd';"
docker exec -it postgresql psql --username=root ranger -c "GRANT ALL PRIVILEGES ON DATABASE druid TO druiddba;"
```

```bash
docker exec -it postgresql psql --username=root dev -c "CREATE DATABASE oozie;" 
docker exec -it postgresql psql --username=root ranger -c "CREATE USER ooziedba WITH PASSWORD 'ooziepwd';"
docker exec -it postgresql psql --username=root ranger -c "GRANT ALL PRIVILEGES ON DATABASE oozie TO ooziedba;"
```

```bash
docker exec -it postgresql psql --username=root dev -c "CREATE DATABASE rangerkms;" 
docker exec -it postgresql psql --username=root ranger -c "CREATE USER rangerkmsdba WITH PASSWORD 'rangerkmspwd';"
docker exec -it postgresql psql --username=root ranger -c "GRANT ALL PRIVILEGES ON DATABASE rangerkms TO rangerkmsdba;"
```
# RUN AMBARI REPO
docker run -dit -h ambari-repo --name ambari-repo --network workbench -p 80 -v /mnt/hgfs/HDP-vm-shared/hortonworks-repo:/usr/local/apache2/htdocs/ httpd:2.4

# scrap ports para exportar na imagem base
```bash
echo 'Criando virtual env' \
  && python -m venv webscraping-ports/.venv \
  && echo 'Ativando virtual env' \
  && source webscraping-ports/.venv/bin/activate \
  && echo 'Executando pip install' \
  && pip install -q -r webscraping-ports/requirements.txt \
  && echo 'Executando script python' \
  && python webscraping-ports/scrap_ports.py > webscraping-ports/ports.txt \
  && echo '' >> webscraping-ports/ports.txt \
  && echo 'Limpando portas' \
  && sed -ri '/## EXPOSE PORTS INIT/,/## EXPOSE PORTS END/!b;//!d' docker/ambari/base/Dockerfile \
  && echo 'Incluindo portas' \
  && sed -ri '/## EXPOSE PORTS INIT/r webscraping-ports/ports.txt' docker/ambari/base/Dockerfile \
  && echo 'Desetivanvo virtual env' \
  && deactivate
```

# BUILD IMAGES
./docker/ambari/base/build.sh
./docker/ambari/server/build.sh
./docker/ambari/agent/build.sh

# RUN AMBARI SERVER
docker run -h ambari-server --name ambari-server --privileged --network workbench -p 8080:8080 -t -d wilker/ambari-server


## Criando base do ambari
```bash
docker exec -i ambari-server /bin/bash -c 'cat /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql' | docker exec -i postgresql bash -c 'psql -U ambaridba ambari -w -a -q -f -'
```

# RUN AMBARI-BASES 
docker run -dit -h ambari-agent-1 --name ambari-agent-1 --privileged --network workbench wilker/ambari-base
docker run -dit -h ambari-agent-2 --name ambari-agent-2 --privileged --network workbench wilker/ambari-base
docker run -dit -h ambari-agent-3 --name ambari-agent-3 --privileged --network workbench wilker/ambari-base
docker run -dit -h ambari-agent-4 --name ambari-agent-4 --privileged --network workbench wilker/ambari-base

# Create cluster

# Get ambari-server ssh-key 
docker exec -it ambari-server bash -c 'cat /root/.ssh/id_rsa'

Target Hosts: ambari-agent-[1-4]
