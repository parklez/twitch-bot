# parky's twitch bot

![logo](https://raw.githubusercontent.com/parklez/twitch-bot/master/parky_bot/resources/banner_new_wide_kitty.png)\
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub top language](https://img.shields.io/github/languages/top/parklez/twitch-bot)
![Made with love](https://img.shields.io/badge/made%20with-love-ff69b4)
![Windows](https://img.shields.io/badge/-windows%20builds-blue) \
An open-souce, minimalistic, cross-platform, easily expandable Twitch IRC/API bot.

### Features
- Connect to Twitch IRC chat.
- Connect to Twitch API via kraken v5 (needs to be updated)
- Play media with python-vlc
- Google's text to speech

### Adding a command is this simple:
Editing `parky_bot/app.py` and adding:
```python
@BOT.decorator('!hello'):
def my_custom_command(message):
    BOT.send_message(f'Howdy {message.sender}!')
 ```
 In the example above, a decorator is responsible to handle which messages trigger which function.

### Dependencies
- VLC (64-bit version)
- Python 3.7 or above
- Few python dependencies:
```sh
pip3 install -r requirements.txt
```

### Running
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