
## Install docker
```bash
sudo apt remove docker docker-engine docker.io containerd runc

sudo apt-get update

sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

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
sed -ri 's/^plugins=\((.*)\)/plugins=\(\1 k3d\)/g' ~/.zshrc
rm -f ~/.zcompdump* && source ~/.zshrc
```

# Instalar programas

## Install lens (kubernetes ui)
```bash
sudo snap install kontena-lens --classic
```