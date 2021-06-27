# Passo a passo

## [Setup Ubuntu](../../ubuntu/docs/setup_linux.md)

## [Setup Docker](../../ubuntu/docs/setup_docker.md)

# Execucao

## Create cluster
```bash
k3d cluster create mycluster

# Criar stack de monitoracao
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```


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

## Criando base do ambari
```bash
docker exec -i ambari-server /bin/bash -c 'cat /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql' | docker exec -i postgresql bash -c 'psql -U ambaridba ambari -w -a -q -f -'
```