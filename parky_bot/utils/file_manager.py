import json
import os
from parky_bot.utils.logger import get_logger


DEFALT_SETTINGS = {
    'irc': {
        'username': 'username',
        'channel': 'channel',
        'token': 'Generate a token at www.twitchapps.com/tmi/',
    },
    'api': {
        'client_id': "client_id https://glass.twitch.tv/console/apps",
        'channel': 'channel',
        'token': "Generate a token with 'user_read channel_editor' scopes at https://twitchapps.com/tokengen/",
    }
}

logger = get_logger()


def create_json(data, file):
    with open(file, "w") as _file:
        json.dump(data, _file, indent=4)

def load_json(file):
    with open(file, "r") as _file:
        return json.load(_file)

def make_dir(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            logger.info(f'The folder {directory} has been created!')
        except Exception:
            logger.critical(f'Could not make "/{directory}"!', exc_info=True)

def create_settings_json(file):
    create_json(DEFALT_SETTINGS, file)
