# parky's twitch bot

![logo](https://raw.githubusercontent.com/parklez/twitch-bot/master/art/banner_new_wide_kitty.png)\
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub top language](https://img.shields.io/github/languages/top/parklez/twitch-bot)
![Made with love](https://img.shields.io/badge/made%20with-love-ff69b4)
[![Build Status](https://travis-ci.org/parklez/twitch-bot.svg?branch=master)](https://travis-ci.org/parklez/twitch-bot)
![Downloads](https://img.shields.io/github/downloads/parklez/twitch-bot/total) \
An open-source, minimalistic, cross-platform, easily expandable with plugins "Twitch IRC/API" bot.

### Features
- 🔌 Connect to Twitch IRC chat!
- 🔌 Connect to Twitch API! (change game, title)
- 🔊 Play custom sounds!
- 🔊 Google's text to speech!
- ⚡ Load your custom made plugins!

### Download for Windows
Get @ [Releases page](https://github.com/parklez/twitch-bot/releases)

### Download for all platforms
Download the repo [Here](https://github.com/parklez/twitch-bot/archive/master.zip) (or using git)

### Making a plugin is this easy:
Copy the template below:
```python
from parky_bot.settings import BOT
from parky_bot.models.message import Message

@BOT.decorator(commands=['!hello', '!hi']):
def my_custom_command(message): 
    BOT.send_message(f'Howdy {message.sender}!')
 ```
Save your `my_custom_plugin.py` under `/plugins` folder and you're ready to go!

### Dependencies
- Python 3.7 or above
- Few python dependencies:
```sh
pip3 install -r requirements.txt
```

### Running
- Download this repository & unzip
- Navigate to the extracted folder
- Install dependencies if you haven't already
- Using your favorite terminal, type the code below:
```sh
python3 -m parky_bot.app
```

### Disclaimer
This project is under heavy development and subject to refactoring and code smells.

### Contributors
- xKittieKat (Artist)
<img src="https://raw.githubusercontent.com/parklez/twitch-bot/master/art/barky_chan.png" width="200" height="200">

### 3rd party resources
- Shiba icon [icon-icons.com](https://icon-icons.com/icon/dog-pet-animal-japanese-shiba-inu-japan/127300)
- Banner [github.com/liyasthomas](https://github.com/liyasthomas/banner)
