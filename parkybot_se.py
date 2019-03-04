#!/usr/bin/env python3

import socket
import re
import time
import datetime
import random

from parkybot.file_manager import *
from parkybot.sfx_and_greetings import *
from parkybot.twitch import *


def message_pooling(irc):
    print("Pooling Chat...")
    data = ""
    
    while True:
        try:
            data = irc.irc_sock.recv(1024).decode('UTF-8')
            #print(data)
            
            if data == "PING :tmi.twitch.tv\r\n":
                irc.send_pong()
            
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
    username = sender.lower()
    
    if sender not in CHATTERS and sender != CHAT.username:
        CHATTERS.append(sender)
    
    if request in commands.keys():
        commands[request](message, sender)
        
    elif request in SFX.sounds:
        SFX.sounds[request].play_sound()
                
    if username in Greeter.people:
        # Another solution is to delete dict keys since they're only used once.
        if Greeter.people[username].greeted == False:
            CHAT.send_message(Greeter.people[username].message)
            if Greeter.people[username].sound != 'null':
                simpleaudio.WaveObject.from_wave_file(Greeter.people[username].sound).play()
            Greeter.people[username].greeted = True    
            
    if username in EDITORS:
        if request == "!game":
            API.update_game(message[6:])
            CHAT.send_message(API.last_call)
            
        if request == "!status":
            API.update_status(message[8:])
            CHAT.send_message(API.last_call)

def api_pooling(twitch_api, irc=None):
    while True:
        followers = twitch_api.check_for_new_followers()
        print("API pooled")
        message = "Thank you "
        if followers:
            for follower in followers:
                message += follower + " Daijoubu , "
            
            message = message[:-2] + ' for following! <3'
            print(message)
            #irc.send_message(message)
        time.sleep(3)
            
            
### Custom Chat Functions
def command_uptime(message=None, sender=None):
    delta = int(time.time() - STARTUP)
    message = "Stream uptime {} h:m:s dogeWink".format(str(datetime.timedelta(seconds=delta)))
    CHAT.send_message(message)

def command_sounds(message=None, sender=None):
    message = ""
    for sfx in sorted(SFX.sounds.keys()):
        message += sfx + ', '
        
    message = message[:-2] + ' dogeKek'
    CHAT.send_message(message)
    
def command_commands(message=None, sender=None):
    CHAT.send_message('My tricks: !sounds, !uptime, !pat, !shoot Daijoubu')

def command_pat(message=None, sender=None):
    message = message.split(' ')
    if len(message) <= 1:
        return
        
    target = message[1].strip('@')
    
    if not target:
        return
        
    if target.lower() == CHAT.username:
        doggos = ('dogeWink', 'dogeKek', 'Wowee', 'WooferWhat')
        CHAT.send_message(random.choice(doggos))
        return
        
    if target.lower() == sender.lower():
        CHAT.send_message('Someone else needs to pat you WanSeeU')
        return
        
    responses = ("{} gives {}'s head a soft pat Daijoubu",
    "{} WanISee // pat pat pat {}",
    "{} slowly strokes {}'s hair LoudDoge",
    "{} messes with {}'s hair PillowYes",
    "{} pats {}'s head and they blush LewdChamp",
    "{} pats {} NepComfy",
    "{} tries to pat {} but they move away KannaSpooks")
    
    CHAT.send_message(random.choice(responses).format(sender, target))
    
def command_shoot(message=None, sender=None):
    message = message.split(' ')
    
    if len(message) <= 1:
        target = None
        
    else:
        target = message[1].strip('@')

    responses = ("{} shoots {} in the face, bloody hell! oie",
    "{0} tries to shoot {1} but {1} dodges and shoots {0} back! oie",
    "{} shoots {} but misses! WotInTarnation",
    "{} fires a rocket at {} leaving only dust left! oie",
    "{} shoots {} with an airsoft gun KappaKappa",
    "{} shoots {}'s brains out KannaSpooks")
    
    temp_chatters = CHATTERS
    temp_chatters.remove(sender)  # Remove sender
    
    if not target:
        if temp_chatters:
            target = random.choice(temp_chatters)
        else:
            return
    if target.lower() == sender.lower():  # Don't allow self-targetting
        return
        
    CHAT.send_message(random.choice(responses).format(sender, target))

def command_hug(message=None, sender=None):
    message = message.split(' ')
    if len(message) <= 1:
        return
        
    target = message[1].strip('@')
    
    if not target:
        return
        
    if target.lower() == CHAT.username:
        return
        
    if target.lower() == sender.lower():
        CHAT.send_message('Someone else needs to hug you WanSeeU')
        return
        
    responses = ("{} hugs {} like it's been forever! PoiHug",
    "{} hugs {} <3 PoiHug",
    "{} wraps arms around {} making them blush LewdChamp",
    "{} hugs {} PillowYes",
    "{} runs towards {} giving them a big hug PillowYes",
    "{} bear hugs {} Daijoubu",
    "{} hugs {} but they break free of it DogeThump")
    
    CHAT.send_message(random.choice(responses).format(sender, target))

def command_tap(message=None, sender=None):
    message = message.split(' ')
    target = message[1].strip('@')
    
    if not target:
        if not CHATTERS:
            return
        else:
            target = random.choice(CHATTERS)
    
    responses = ("{} taps {} ass",
                 "{} rips {} dick off oie")
                 
    CHAT.send_message(random.choice(responses).format(sender, target))

def command_love(message=None, sender=None):
    target = message.split("!love")[1]
    
    if not target:
        return
        
    else:
        target = target[1:]
    
    CHAT.send_message("There's {}% of love between {} and {}".format(random.randrange(0, 100), sender, target))
    
#TODO: Create a wrapper instead of this dict
commands = {
           '!commands': command_commands,
           '!pat': command_pat,
           '!sfx': command_sounds,
           '!shoot': command_shoot,
           '!sounds': command_sounds,
           '!uptime': command_uptime,
           '!hug': command_hug,
           '!love': command_love,
            }

CHATTERS = list()
STARTUP = time.time()
EDITORS = ['leparklez']

settings = load_json("data/settings.json")
CHAT = TwitchIRC(settings['irc']['username'], settings['irc']['channel'], settings['irc']['token'])
API = TwitchAPI(settings['api']['client_id'], settings['api']['channel'], settings['api']['token'])

sounds_json = load_json("data/sounds.json")
for key in sounds_json['global']:
    SFX(key['command'], key['path'])
    
users_json = load_json("data/users.json")
for key in users_json['users']:
    Greeter(key['username'], key['message'], key['sound'])

#TODO: Update twitch.API so that we can properly retrieve updated information without requests
def print_status(API):
    print("---- ParkyBot: Special Edition 0.2\n")
    print("Channel:", API.channel_info["name"], "ID:", API.channel_info["_id"])
    print("Status:", API.channel_info["status"])
    print("Game:", API.channel_info["game"])
    print("Followers:", API.channel_info["followers"], "Views:", API.channel_info["views"])
    print("----")
        
print_status(API)
message_pooling(CHAT)
