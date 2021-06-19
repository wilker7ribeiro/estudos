# Passo a passo
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
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
sudo apt install build-essential
brew install gcc
```
```bash
sudo gedit ~/.zshrc
# add to the end
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
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
```
```
sudo gedit ~/.zshrc
# add to the plugins
plugins=(... docker docker-compose) 

source ~/.zshrc
```
## Install k3d
```bash
curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash

k3d -h

# add zsh completion
mkdir -p ~/.oh-my-zsh/custom/plugins/k3d
k3d completion zsh > ~/.oh-my-zsh/custom/plugins/k3d/_k3d
rm -f ~/.zcompdump* && source ~/.zshrc

k3d cluster create mycluster
```
## Install Kubectl e Kubectx
```bash
brew install kubectl
brew install kubectx
```
```bash
sudo gedit ~/.zshrc
# add to the plugins
.zshrc plugins=(... kubectl kubectx)

source ~/.zshrc
```

## Install helm
```bash
brew install helm
```

## Install lens
```bash
snap install kontena-lens --classic
```

## Install vscode
```bash
sudo snap install --classic code
```

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```

# create network workbench
```bash
docker network create workbench \
  --subnet 10.1.1.0/24
```

# create postgress
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
```