#!/usr/bin/env python3

import re
import socket
import time
import datetime
import random

import requests
import simpleaudio


SOUNDS = {
        '!crow': 'sounds/crow.wav',
        '!owee': 'sounds/owee.wav',
        }

GREETINGS = {
        'friend1': 'Welcome friend1!',
        'friend2': 'I see you here friend2!',
        }
        
EDITORS = (
        'MyTwitchChannel',
        'MyTrustyMod',
        )
            
# ------------------------------------------- IRC Settings -------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = "#MyTwitchChannel"                       # Channelname = #{Nickname}
NICK = "MyBotOrChannel"                         # Nickname = Twitch username
PASS = ""                                       # www.twitchapps.com/tmi/ will help to retrieve the required authkey

# -------------------------------------------- Twitch API --------------------------------------------
CLIENT_ID = ''                               # Your bot's client_id https://glass.twitch.tv/console/apps
URL = 'https://api.twitch.tv/kraken/'
CHANNEL_ID = ''                              # get_id() can help retrieving this info
OAUTH_KEY = ''                               # https://twitchapps.com/tokengen/ for "user_read channel_editor"

HEADERS = {
        'Client-ID': CLIENT_ID,
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Authorization': 'OAuth ' + OAUTH_KEY
        }
        
def update_game(game_title):
    game_title = game_title[6:]
    data = {'game': game_title}
    post_data = {'channel': data}
    response = requests.put(URL + 'channels/' + CHANNEL_ID, json=post_data, headers=HEADERS)
    
    if response.status_code == 200:
        send_message(CHAN, 'Game updated: ' + game_title)
    else:
        print(response.text)

def update_status(stream_title):
    stream_title = stream_title[7:]
    data = {'status': stream_title}
    post_data = {'channel': data}
    response = requests.put(URL + 'channels/' + CHANNEL_ID, json=post_data, headers=HEADERS)

    if response.status_code == 200:
        send_message(CHAN, 'Status updated: ' + stream_title)
    else:
        print(response.text)

def get_id(username):
    r = requests.get(URL + 'users?login=' + username, headers=HEADERS)
    print(r.json())

# --------------------------------------------- Classes ----------------------------------------------
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
            
            
# ----------------------------------------- Basic Functions ------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))

def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))

def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))

def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))

def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))

# ---------------------------------------- Parsing Functions -----------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result

def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result

def parse_message(msg, sender):
    if sender not in CHATTERS and sender != NICK:
        CHATTERS.append(sender)
    
    # msg string always ends with an space, so the list below ends with an empty <string> object which means False in bool()
    if len(msg) >= 1:
        full = msg[:-1]
        msg = msg.split(' ')
        
        OPTIONS = {
           '!commands': command_commands,
           '!pat': command_pat,
           '!sfx': command_sounds,
           '!shoot': command_shoot,
           '!sounds': command_sounds,
           '!uptime': command_uptime,
            }
                   
        if msg[0] in OPTIONS:
            OPTIONS[msg[0]](sender, msg[1])
            
        if msg[0] in SOUNDS:
            for sfx in SFX.sounds:
                if sfx.command == msg[0]:
                    sfx.play_sound()
                    
        if sender.lower() in GREETINGS:
            for item in Greeter.people:
                if item.username.lower() == sender.lower():
                    if item.greeted == False:
                        send_message(CHAN, item.message)
                        item.greeted = True
                            
        if sender.lower() in EDITORS:
            if msg[0] == "!game":
                update_game(full)
            if msg[0] == "!status":
                update_status(full)

# ------------------------------------------ Bot Functions -------------------------------------------
def command_uptime(sender=None, target=None):
    delta = int(time.time() - STARTUP)
    message = "Stream uptime {} h:m:s dogeWink".format(str(datetime.timedelta(seconds=delta)))
    send_message(CHAN, message)

def command_sounds(sender=None, target=None):
    message = ""
    for sfx in sorted(SOUNDS.keys()):
        message += sfx + ', '
        
    message += 'dogeKek'
    send_message(CHAN, message)
    
def command_commands(sender=None, target=None):
    send_message(CHAN, 'My tricks: !sounds, !uptime, !pat, !shoot dogeKek')

# --------------------------------------------- Startup ----------------------------------------------
STARTUP = time.time()
CHATTERS = list()

for key in SOUNDS:
    SFX(key, SOUNDS[key])
    
for key in GREETINGS:
    Greeter(key, GREETINGS[key])

# -------------------------------------------- Main Loop ---------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))
#con.settimeout(0.1) # Helps main loop but I don't know how to handle this properly.

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""

while True:

    time.sleep(0.05) # 20 request per second?
    
    try:
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    parse_message(message, sender)

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
