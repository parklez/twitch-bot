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
    #pylint: disable=no-member
    RESOURCE_PATH = sys._MEIPASS
else:
    APP_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir)
    RESOURCE_PATH = os.path.join(os.path.dirname(__file__))
SETTINGS_PATH = os.path.join(APP_PATH, 'settings.json')
SOUNDS_PATH = os.path.join(APP_PATH, 'sounds')

# Loading settings
SETTINGS = get_settings(SETTINGS_PATH)

# Configure logger
configure_logger(get_logger(), int(SETTINGS['logging']['level']))

# Initilizing bot
IRC = TwitchIRC(SETTINGS['irc']['username'],
                SETTINGS['irc']['channel'],
                SETTINGS['irc']['token'])
API = TwitchAPI(SETTINGS['api']['client_id'],
                SETTINGS['api']['channel'],
                SETTINGS['api']['token'])
BOT = ParkyBot(API, IRC)

def start():
    if '--console' not in sys.argv:
        threading.Thread(target=Application, args=(BOT, SETTINGS)).start()
    BOT.pooling()
    save_settings(SETTINGS, SETTINGS_PATH)
