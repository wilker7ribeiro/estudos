# Passo a passo

# Instalar libs
## Install ZSH
```bash
sudo apt update
sudo apt upgrade
sudo apt install -y curl wget git zsh xclip
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
chsh -s $(which zsh)
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
sudo apt install -y build-essential
brew install gcc
```
```bash
```

## install hostess (add itens to /etc/hosts)
```bash
brew install hostess
```

# Instalar programas

## Install vscode
```bash
sudo snap install --classic code
```

## Install dbeaver
```bash
sudo snap install dbeaver-ce
```

## PyEn
```bash
sudo apt-get update; sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

git clone https://github.com/pyenv/pyenv.git ~/.pyenv

cd ~/.pyenv && src/configure && make -C src

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init --path)"' >> ~/.profile

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zprofile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zprofile
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc

sed -ri 's/^plugins=\((.*)\)/plugins=\(\1 pyenv\)/g' ~/.zshrc

pyenv install 3.9.6
pyenv global 3.9.6
```