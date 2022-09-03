# parky's twitch bot
<p align="center">
  <img src="https://raw.githubusercontent.com/parklez/twitch-bot/master/img/win10.png">
</p>
A free, minimal, lightweight, cross-platform, easily expandable Twitch IRC/API bot.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Made with love](https://img.shields.io/badge/made%20with-love-ff69b4)
![Downloads](https://img.shields.io/github/downloads/parklez/twitch-bot/total)

## Features
- 🔌 Connect to Twitch IRC chat!
- 🔌 Connect to Twitch API! (change game, title)
- 🔊 Play custom sounds!
- ⚡ Make your own plugins with 5 lines of Python code! 🐍

## Windows (8, 8.1, 10) 💾
Get @ [Releases page](https://github.com/parklez/twitch-bot/releases)

## Linux 🐧
You may use the following live script to install this app on your machine.\
Open a terminal and choose your favourite method below to install:
#### Using "wget"
```sh
sh -c "$(wget https://raw.githubusercontent.com/parklez/twitch-bot/master/scripts/install.sh -O -)"
```
#### Using "curl"
```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/parklez/twitch-bot/master/scripts/install.sh)"
```
## MacOS 🍎
See [running locally](#running-locally) below.

## ⚡ Included plugins
|Plugin           |Commands            |
|-----------------|--------------------|
|Custom commands  | !add <!command> < response >|
|Google's TTS     | !tts, !< language >|
|Misc             | !commands, !remind < something >|
|Pat & Love       | !pat, !love < someone >|
|Plugin toggle    | !plugin < disable/enable > <!command>|
|Sounds¹          | !< file_name >|
|Twitch API²      | !uptime, !game < optional >, !title/!status < optional >|

[1]: Custom sounds go inside `/sounds` in mp3/wav formats.\
[2]: One must fulfill API credentials inside the application settings. 

## 💡 Simple plugin example
Copy the template below:
```python
from parky_bot.settings import BOT
from parky_bot.models.message import Message

@BOT.decorator(commands=['!hello', '!hi']):
def my_custom_command(message): 
    BOT.send_message(f'Howdy {message.sender}!')
 ```
Save your `my_custom_plugin.py` under `/plugins` folder and you're ready to go!

## Running locally
- Install Python 3.7 or newer
- Set up a virtual env (optional):
```sh
python -m venv .venv
# Unix
source .venv/bin/activate

# Windows
.venv/Scripts/Activate.ps1
```
- Install dependencies:
```sh
pip install -r requirements.txt

# MacOS Only:
pip install pyobjc tkmacosx
```
- Start the application:
```sh
python -m parky_bot.app
# Console only/No tkinter:
python -m parky_bot.app --console
```

# Linting
This project uses `autopep8` for linting. Subject to change.

## Disclaimer
This project is under heavy development and subject to refactoring and code smells.

## Contributors
- xKittieKat (Artist) [deviantart.com](https://www.deviantart.com/xkittiekat/art/barky-chan-v-1-856512308)

## 3rd party resources
- Volume icon [icon-icons.com](https://icon-icons.com/icon/volume-up-interface-symbol/73337)
- Shiba icon [icon-icons.com](https://icon-icons.com/icon/dog-pet-animal-japanese-shiba-inu-japan/127300)
- Menu icon [icons-icons.com](https://icon-icons.com/icon/menu/71858)
- Banner [github.com/liyasthomas](https://github.com/liyasthomas/banner)
