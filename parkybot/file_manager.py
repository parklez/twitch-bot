import json
import os


def create_json(data, file):
    with open(file, "w") as _file:
        json.dump(data, _file, indent=4)
        
def load_json(file):
    'Returns a dictionary from a json file.'
    with open(file, "r") as _file:
        return dict(json.load(_file))

def create_default_json(file="settings.json"):
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
        
def create_default_sounds_json(file="sounds.json"):
    data = {
        'global': {
            '!command': 'path to file.wav',
            }
        }
    create_json(data, file)
    
def create_default_users(file="users.json"):
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
