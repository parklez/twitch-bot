import json
import os


DEFAULT_SETTINGS = {
    'irc': {
        'channel': '',
        'token': '',
        'scopes': 'chat:read+chat:edit'
    },
    'api': {
        'client_id': 'https://dev.twitch.tv/console/apps',
        'token': '',
        'scopes': 'channel:read:editors+channel:manage:broadcast+user:read:email'
    },
    'logging': {
        'level': 20
    },
    'settings': {
        'volume': 80,
        'font-size': 11
    }
}


def create_json(data: dict, file: str) -> None:
    with open(file, 'w') as _file:
        json.dump(data, _file, indent=4)


def load_json(file: str) -> dict:
    with open(file, 'r') as _file:
        return json.load(_file)


def make_dir(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_settings_json(file: str) -> dict:
    create_json(DEFAULT_SETTINGS, file)


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
            get_settings.single = DEFAULT_SETTINGS
    return get_settings.single


get_settings.single = None


def save_settings(data: dict, file: str) -> None:
    create_json(data, file)
