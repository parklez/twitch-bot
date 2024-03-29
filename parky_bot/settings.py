import os
import sys
import threading
from parky_bot.gui.main_window import Application
from parky_bot.utils.file_manager import get_settings, save_settings
from parky_bot.twitch.irc import TwitchIRC
from parky_bot.twitch.api import TwitchAPI
from parky_bot.twitch.bot import ParkyBot
from parky_bot.utils.logger import get_logger, configure_logger


# Setting paths
if getattr(sys, 'frozen', False):
    APP_PATH = os.path.dirname(sys.executable)
else:
    APP_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir)
SETTINGS_PATH = os.path.join(APP_PATH, 'settings.json')
SOUNDS_PATH = os.path.join(APP_PATH, 'sounds')

# Loading settings
SETTINGS = get_settings(SETTINGS_PATH)


def app_running():
    return app_running.state


app_running.state = True

# Configure logger
configure_logger(get_logger(), int(SETTINGS['logging']['level']))

# Initilizing bot
IRC = TwitchIRC(SETTINGS['api']['client_id'],
                SETTINGS['irc']['channel'],
                SETTINGS['irc']['token'])
API = TwitchAPI(SETTINGS['api']['client_id'],
                SETTINGS['api']['token'])
BOT = ParkyBot(IRC, API)


def start():
    if '--console' in sys.argv:
        BOT.pooling()
    else:
        threading.Thread(target=BOT.pooling).start()
        Application(BOT, SETTINGS)
    save_settings(SETTINGS, SETTINGS_PATH)
    app_running.state = False
