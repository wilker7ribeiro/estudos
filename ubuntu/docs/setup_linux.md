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

# Instalar programas

## Install vscode
```bash
sudo snap install --classic code
```

## Install dbeaver
```bash
sudo snap install dbeaver-ce
```
