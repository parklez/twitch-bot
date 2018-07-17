#!/usr/bin/env python3

###################################
BOT_NICKNAME = ""
CHANNEL_NICKNAME = ""
IRC_TOKEN = "" # Get your access token here www.twitchapps.com/tmi/

API_CLIENT_ID = "" # Get your bot application client_id here https://glass.twitch.tv/console/apps
API_CHANNEL_NICKNAME = CHANNEL_NICKNAME
API_TOKEN = "" # Get your token at https://twitchapps.com/tokengen/ for "user_read channel_editor" scopes.
###################################

import socket
import re
import time
import datetime
import os

import requests
import simpleaudio

GREETINGS = {
        'friend1': 'Welcome friend1!',
        'friend2': 'I see you here friend2!',
        }
        
EDITORS = (
        'MyTwitchChannel',
        'MyTrustyMod',
        )


class TwitchIRC:
    def __init__(self, username, channel, token):
        self.username = username
        self.token = token
        self.channel = '#' + channel
        self.host = 'irc.twitch.tv'
        self.port = 6667
        self._sock = socket.socket()
        self.welcome()

    def welcome(self):
        """
        This function connects to twitch IRC, sends password, nickname and joins a channel.
        """
        self._sock.connect((self.host, self.port))
        self.send_pass()
        self.send_nick()
        self.join_channel()

    def disconnect(self):
        self._sock.close()
        
    def send(self, data):
        """
        This function converts data into bytes with UTF-8 encoding then socket.send()
        """
        self._sock.send(bytes(data, 'UTF-8'))

    def send_pong(self):
        self.send("PONG :tmi.twitch.tv\r\n")

    def send_nick(self):
        self.send("NICK {}\r\n".format(self.username))

    def send_pass(self):
        self.send("PASS {}\r\n".format(self.token))

    def join_channel(self):
        self.send("JOIN {}\r\n".format(self.channel))

    def part_channel(self):
        self.send("PART {}\r\n".format(self.channel))

    def send_message(self, message):
        self.send("PRIVMSG {} :{}\r\n".format(self.channel, message))


class TwitchAPI:
    def __init__(self, client_id, channel, token=None):
        """
        Basic Twitch API calls using kraken v5
        
        client_id = client id from your bot application <string> https://glass.twitch.tv/console/apps
        token = token for "user_read channel_editor" scopes <string> https://twitchapps.com/tokengen/
        channel = username of the channel authorized above <string>
        """
        self.client_id = client_id
        self.token = token
        self.channel = channel
        self.base_api = "https://api.twitch.tv/kraken/"
        self.last_call = ""
        
        self.headers = {'Client-ID': self.client_id,
                        'Accept': 'application/vnd.twitchtv.v5+json'}
                        
        if self.token:
            self.headers['Authorization'] = 'OAuth ' + self.token
            
        self.channel_id = self.get_channel_id()
        
    def get_channel_id(self):
        r = requests.get(self.base_api + 'users?login=' + self.channel, headers=self.headers)
        if r.status_code == 200:
            return r.json()['users'][0]['_id']
        else:
            print('[Twitch API]', r.text)
            
    def update_game(self, game_title):
        data = {'game': game_title}
        post_data = {'channel': data}
        response = requests.put(self.base_api + 'channels/' + self.channel_id, json=post_data, headers=self.headers)
        
        if response.status_code == 200:
            self.last_call = 'Game updated: ' + game_title
        else:
            self.last_call = response.text

    def update_status(self, stream_title):
        data = {'status': stream_title}
        post_data = {'channel': data}
        response = requests.put(self.base_api + 'channels/' + self.channel_id, json=post_data, headers=self.headers)

        if response.status_code == 200:
            self.last_call = 'Status updated: ' + stream_title
        else:
            self.last_call = response.text
            

class SFX:
    
    sounds = list()
    
    def __init__(self, command, path, cooldown=False):
        self.command = command
        self.path = path
        self.sound = simpleaudio.WaveObject.from_wave_file(path)
        self.cooldown = cooldown
        self.lastplayed = 0
        SFX.sounds.append(self)
        
    def play_sound(self):
        if self.cooldown:
            return ## TODO
            
        else:
            self.sound.play()
            
            
class Greeter:

    people = list()
    
    def __init__(self, username, message):
        self.username = username
        self.message = message
        self.greeted = False
        Greeter.people.append(self)

        
def message_pooling(chat):
    data = ""
    
    while True:
        time.sleep(0.1)
        
        try:
            data = chat._sock.recv(1024).decode('UTF-8')
            #print(data)
            
            if data == "PING :tmi.twitch.tv\r\n":
                chat.send_pong()
            
            if data.split(' ')[1] == 'PRIVMSG':
                username = re.search(r"\w+", data).group(0)
                message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :").sub("", data).rstrip('\n').rstrip()
                parse_message(message, username)
                #print(time.strftime("[%H:%M]"), username + ': ' + message)
                
            data = ""

        except socket.error:
            print("Socket died")

        except socket.timeout:
            print("Socket timeout")
 
def parse_message(message, sender):

    request = message.lower().split()[0]
    
    if sender not in CHATTERS and sender != CHAT.username:
        CHATTERS.append(sender)
    
    commands = {
               '!commands': command_commands,
               '!sfx': command_sounds,
               '!sounds': command_sounds,
               '!uptime': command_uptime,
               '!ping': command_ping,
                }
    
    if request in commands.keys():
        commands[request](message, sender)
        
    if request in SOUNDS:
        for sfx in SFX.sounds:
            if sfx.command == request:
                sfx.play_sound()
                
    if sender.lower() in GREETINGS:
        for item in Greeter.people:
            if item.username == sender.lower():
                if item.greeted == False:
                    CHAT.send_message(item.message)
                    item.greeted = True
                    ## Hardcode oie
                    if item.username == 'sayan3':
                        simpleaudio.WaveObject.from_wave_file('sounds/sayan.wav').play()
                        
    if sender.lower() in EDITORS:
        if request == "!game":
            API.update_game(message[6:])
            CHAT.send_message(API.last_call)
            
        if request == "!status":
            API.update_status(message[7:])
            CHAT.send_message(API.last_call)
    
########## Bot Functions
def command_uptime(message=None, sender=None):
    delta = int(time.time() - STARTUP)
    message = "Stream uptime {} h:m:s dogeWink".format(str(datetime.timedelta(seconds=delta)))
    CHAT.send_message(message)

def command_sounds(message=None, sender=None):
    message = ""
    for sfx in sorted(SOUNDS.keys()):
        message += sfx + ', '
        
    message = message[:-2] + ' dogeKek'
    CHAT.send_message(message)
    
def command_commands(message=None, sender=None):
    CHAT.send_message('My tricks: !sounds, !uptime, !ping dogeKek')

def command_ping(message=None, sender=None):
    CHAT.send_message('pong!')
    
########## Startup
CHAT = TwitchIRC(BOT_NICKNAME, CHANNEL_NICKNAME, IRC_TOKEN)
API = TwitchAPI(API_CLIENT_ID, API_CHANNEL_NICKNAME, API_TOKEN)
CHATTERS = list()
STARTUP = time.time()
SOUNDS = {}

for file in os.listdir('sounds'):
    SOUNDS["!" + file[:-4]] = 'sounds/' + file
    
for key in SOUNDS:
    SFX(key, SOUNDS[key])
    
for key in GREETINGS:
    Greeter(key, GREETINGS[key])


if __name__ == "__main__":
    message_pooling(CHAT)