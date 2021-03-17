import json
import os


DEFALT_SETTINGS = {
    'irc': {
        'username': '',
        'channel': '',
        'token': 'Generate a token at www.twitchapps.com/tmi/',
    },
    'api': {
        'client_id': "client_id https://glass.twitch.tv/console/apps",
        'channel': '',
        'token': "Generate a token with 'user_read channel_editor' scopes at https://twitchapps.com/tokengen/",
    },
    'logging': {
        'level': 20
    },
    'settings':{
        'volume': 80,
    }
}


def create_json(data: dict, file: str) -> None:
    with open(file, "w") as _file:
        json.dump(data, _file, indent=4)

def load_json(file: str) -> dict:
    with open(file, "r") as _file:
        return json.load(_file)

def make_dir(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_settings_json(file: str) -> dict:
    create_json(DEFALT_SETTINGS, file)

def get_settings(file: str) -> dict:
    """Gets a dict containing the application settings as singleton*.
    *The singleton aspect is nowhere necessary in this application,
    but at least prevents re-reading the file from disk.

    Args:
        file (str): Path to settings file, if not found, will create a default one.

    Returns:
        dict: Settings dict.
    """
    if get_settings.single is None:
        try:
            get_settings.single = load_json(file)
        except FileNotFoundError:
            create_settings_json(file)
            get_settings.single = DEFALT_SETTINGS
    return get_settings.single

get_settings.single = None

def save_settings(data: dict, file: str) -> None:
    create_json(data, file)
