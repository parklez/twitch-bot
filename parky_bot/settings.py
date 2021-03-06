import os
import sys
import threading
from parky_bot.gui.window import Application
from parky_bot.utils.file_manager import load_json, create_settings_json
from parky_bot.twitch.irc import TwitchIRC
from parky_bot.twitch.api import TwitchAPI
from parky_bot.twitch.bot import ParkyBot
from parky_bot.utils.logger import get_logger, configure_logger


# Setting paths
if getattr(sys, 'frozen', False):
    APP_PATH = os.path.dirname(sys.executable)
    #pylint: disable=no-member
    RESOURCE_PATH = sys._MEIPASS
elif __file__:
    APP_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir)
    RESOURCE_PATH = os.path.join(os.path.dirname(__file__))
else:
    raise NotImplementedError

SETTINGS_PATH = os.path.join(APP_PATH, 'settings.json')
SOUNDS_PATH = os.path.join(APP_PATH, 'sounds')

if not os.path.isfile(SETTINGS_PATH):
    create_settings_json(SETTINGS_PATH)
    print('You must write all your info under "settings.json" before continuing!')
    input('press [ENTER] to exit.')
    exit()

SETTINGS = load_json(SETTINGS_PATH)
LOGGING_LEVEL = int(SETTINGS['logging']['level'])
LOGGER = get_logger()
configure_logger(LOGGER, LOGGING_LEVEL)

# Initilizing bot
IRC = TwitchIRC(SETTINGS['irc']['username'],
                SETTINGS['irc']['channel'],
                SETTINGS['irc']['token'])
API = TwitchAPI(SETTINGS['api']['client_id'],
                SETTINGS['api']['channel'],
                SETTINGS['api']['token'])
BOT = ParkyBot(API, IRC)
APP = threading.Thread(target=Application, args=(BOT,))
