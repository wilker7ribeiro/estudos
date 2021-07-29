# Passo a passo

# Instalar libs
## Install ZSH
```bash
sudo apt update
sudo apt upgrade
sudo apt install curl wget git zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sudo chsh "$USER" -s /bin/zsh
sudo su - "$USER"
```

## Installing ZSH Plugins
```bash
git clone 'https://github.com/zsh-users/zsh-autosuggestions.git' "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
sed -ri 's/^plugins=\((.*)\)/plugins=\(\1 zsh-autosuggestions\)/g' ~/.zshrc

git clone 'https://github.com/zsh-users/zsh-completions.git' "$ZSH_CUSTOM/plugins/zsh-completions"
sed -ri 's/^plugins=\((.*)\)/plugins=\(\1 zsh-completions\)/g' ~/.zshrc

git clone 'https://github.com/zsh-users/zsh-history-substring-search.git' "$ZSH_CUSTOM/plugins/history-substring-search"
sed -ri 's/^plugins=\((.*)\)/plugins=\(\1 history-substring-search\)/g' ~/.zshrc

git clone 'https://github.com/zsh-users/zsh-syntax-highlighting.git' "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
sed -ri 's/^plugins=\((.*)\)/plugins=\(\1 zsh-syntax-highlighting\)/g' ~/.zshrc

source ~/.zshrc
```
## Install brew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/wilker/.zprofile
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.zshrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
sudo apt install build-essential
brew install gcc
```
```bash
```

## install hostess
```bash
brew install hostess
```

## Install docker
```bash
sudo apt remove docker docker-engine docker.io containerd runc

sudo apt-get update

sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \\n  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \\n  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker 
docker run hello-world
docker ps
sed -ri 's/^plugins=\((.*)\)/plugins=\(\1 docker docker-compose\)/g' ~/.zshrc
source ~/.zshrc
```
## Install Kubectl e Kubectx
```bash
brew install kubectl
brew install kubectx
sed -ri 's/^plugins=\((.*)\)/plugins=\(\1 kubectl kubectx\)/g' ~/.zshrc
source ~/.zshrc
```

## Install helm
```bash
brew install helm
```

## Install k3d
```bash
curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash

k3d -h

# add zsh completion
mkdir -p ~/.oh-my-zsh/custom/plugins/k3d
k3d completion zsh > ~/.oh-my-zsh/custom/plugins/k3d/_k3d
rm -f ~/.zcompdump* && source ~/.zshrc

```

# Instalar programas

## Install lens
```bash
sudo snap install kontena-lens --classic
```

## Install vscode
```bash
sudo snap install --classic code
```

## Install dbeaver
```bash
sudo snap install dbeaver-ce
```

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



## Criando base do ambari
```bash
docker exec -i ambari-server /bin/bash -c 'cat /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql' | docker exec -i postgresql bash -c 'psql -U ambaridba ambari -w -a -q -f -'
```