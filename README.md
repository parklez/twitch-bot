# parky's twitch bot

![logo](https://raw.githubusercontent.com/parklez/twitch-bot/master/parky_bot/resources/banner_new_wide_kitty.png)\
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub top language](https://img.shields.io/github/languages/top/parklez/twitch-bot)
![Made with love](https://img.shields.io/badge/made%20with-love-ff69b4)
![Windows](https://img.shields.io/badge/-windows%20builds-blue)
![Downloads](https://img.shields.io/github/downloads/parklez/twitch-bot/total) \
An open-source, minimalistic, cross-platform, easily expandable with plugins "Twitch IRC/API" bot.

### Features
- 🔌 Connect to Twitch IRC chat!
- 🔌 Connect to Twitch API! (change game, title)
- 🔊 Play custom sounds/media using VLC!
- 🔊 Google's text to speech!
- ⚡ Load your custom made plugins!

### Making a plugin is this easy!
Copy the template below:
```python
from parky_bot.settings import BOT
from parky_bot.models.message import Message

@BOT.decorator('!hello'):
def my_custom_command(message): 
    BOT.send_message(f'Howdy {message.sender}!')
 ```
Save your `my_custom_plugin.py` under `/plugins` folder and you're ready to go!

### Dependencies
- VLC (64-bit version) [download](https://www.videolan.org/vlc/)
- Python 3.7 or above
- Few python dependencies:
```sh
pip3 install -r requirements.txt
```

### Running
- Download this repository & unzip
- Navigate to the extracted folder
- Using your favorite terminal, type the code below:
```sh
python3 -m parky_bot.app
```

### Disclaimer
This project is under heavy development and subject to refactoring and code smells.

### Contributors
- Energia (Artist) [Twitter](https://twitter.com/JiXiStigma) [Twitch](https://www.twitch.tv/energiaaurea)
<img src="https://raw.githubusercontent.com/parklez/twitch-bot/master/parky_bot/resources/parkchar.png" width="200" height="180">

- xKittieKat (Artist)
<img src="https://raw.githubusercontent.com/parklez/twitch-bot/master/parky_bot/resources/barky_chan.png" width="200" height="200">

### 3rd party resources
- Shiba icon [icon-icons.com](https://icon-icons.com/icon/dog-pet-animal-japanese-shiba-inu-japan/127300)
- Banner [github.com/liyasthomas](https://github.com/liyasthomas/banner)
