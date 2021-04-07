# parky's twitch bot

![screenshot](/art/windows10.png)\
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub top language](https://img.shields.io/github/languages/top/parklez/twitch-bot)
![Made with love](https://img.shields.io/badge/made%20with-love-ff69b4)
[![Build Status](https://www.travis-ci.com/parklez/twitch-bot.svg?branch=master)](https://www.travis-ci.com/parklez/twitch-bot)
![Downloads](https://img.shields.io/github/downloads/parklez/twitch-bot/total) \
An open-source, minimalistic, lightweight, cross-platform, easily expandable with plugins Twitch IRC/API bot.

### Features
- 🔌 Connect to Twitch IRC chat!
- 🔌 Connect to Twitch API! (change game, title)
- 📝 Read chat
- 🔊 Play custom sounds!
- ⚡ Make your own plugins with 5 lines of code!

### Download for Windows (8, 8.1, 10)
Get @ [Releases page](https://github.com/parklez/twitch-bot/releases)

### Download for all platforms
Download the repo [Here](https://github.com/parklez/twitch-bot/archive/master.zip) (or using git) and [run it locally.](#running-locally)

### ⚡ Included plugins
|Plugin       |Commands            |
|-------------|--------------------|
|Google's TTS | !tts, !< language >|
|Misc         | !commands, !remind < something >|
|Pat & Love   | !pat, !love < someone >|
|Plugin toggle| !plugin < disable/enable > <!command>|
|Sounds¹      | !< file_name >|
|Twitch API²  | !uptime, !game < optional >, !title/!status < optional >|

[1]: Custom sounds go inside `/sounds` in mp3/wav formats.\
[2]: One must fulfill API credentials inside the application settings. 

### 💡 Simple plugin example
Copy the template below:
```python
from parky_bot.settings import BOT
from parky_bot.models.message import Message

@BOT.decorator(commands=['!hello', '!hi']):
def my_custom_command(message): 
    BOT.send_message(f'Howdy {message.sender}!')
 ```
Save your `my_custom_plugin.py` under `/plugins` folder and you're ready to go!

### Running locally
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
```
- Start the application:
```sh
python -m parky_bot.app
# Console only/No tkinter:
python -m parky_bot.app --console
```

### Disclaimer
This project is under heavy development and subject to refactoring and code smells.

### Contributors
- xKittieKat (Artist)
<img src="https://raw.githubusercontent.com/parklez/twitch-bot/master/art/barky_chan.png" width="200" height="200">

### 3rd party resources
- Volume icon [icon-icons.com](https://icon-icons.com/icon/volume-up-interface-symbol/73337)
- Shiba icon [icon-icons.com](https://icon-icons.com/icon/dog-pet-animal-japanese-shiba-inu-japan/127300)
- Banner [github.com/liyasthomas](https://github.com/liyasthomas/banner)
