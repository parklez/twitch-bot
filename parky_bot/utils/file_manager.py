import json
import os


def create_json(data, file):
    with open(file, "w") as _file:
        json.dump(data, _file, indent=4)
        
def load_json(file):
    'Returns a dictionary from a json file.'
    with open(file, "r") as _file:
        return dict(json.load(_file))

def create_default_json(file="data/settings.json"):
    data = {
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
    create_json(data, file)
        
def create_default_sounds_json(file="data/sounds.json"):
    data = {
        'global': [
                {
                    "command": "!example",
                    "path": "sounds/hi.wav",
                    "cooldown": "0"
                }
            ]
        }
    create_json(data, file)
    
def create_default_users(file="data/users.json"):
    data = {
        'users': [
            {
                'username': 'person1',
                'message': 'love you senpai',
                'sound': 'null',
            },
            {
                'username': 'person2',
                'message': 'howdy person2',
                'sound': 'null',
            }
        ]
        }
    create_json(data, file)

def sound_files_to_dict(folder):
    data = {'global': []}
    for file in os.listdir(folder):
        if file.endswith('.wav'):
            data['global'].append(
                {'command': '!' + file[:-4].lower(),
                'path': 'sounds/' + file,
                'cooldown': '0'
                }
            )

def make_dir(folder_name):
    'Creates a folder.'
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)
            print('The folder', folder_name, 'has been created!')
        except Exception as e:
            print(e)
