from timeit import default_timer as timer
import os
os.system('mode con: cols=70 lines=20')

start = timer()

import parkybot
from parkybot.sfx_and_greetings import *
from parkybot.file_manager import *
from parkybot.twitch import *

# Loading up settings
if os.path.isfile("data/settings.json"):
    settings = load_json("data/settings.json")
else:
    make_dir('data')
    create_default_json()
    print('Fill in settings within "data/settings.json".')
    input()
    quit()

irc = TwitchIRC(settings['irc']['username'], settings['irc']['channel'], settings['irc']['token'])
api = TwitchAPI(settings['api']['client_id'], settings['api']['channel'], settings['api']['token'])
bot = parkybot.ParkyBot(twitch = api, irc = irc)

# Adding custom chat functionality
print('----------------------------')
import random

@bot.decorator('!uptime')
def command_uptime(message):
    time = bot.twitch.get_uptime()
    bot.send_message(time)

@bot.decorator('!pat')
def command_pat(message):
    if not message.targets:
        target = message.message[5:]
        if not target:
            return
    else:
        target = message.targets[0]
    
    if target.lower() == bot.irc.username.lower():
        doggos = ('dogeWink', 'dogeKek', 'Wowee', 'WooferWhat')
        bot.send_message(random.choice(doggos))
        return
        
    if target.lower() == message.sender.lower():
        bot.send_message("WanISee // {} pat pat pat".format(message.sender))
        return
        
    responses = ("{} gives {}'s head a soft pat Daijoubu",
    "{} WanISee // pat pat pat {}",
    "{} slowly strokes {}'s hair LoudDoge",
    "{} messes with {}'s hair PillowYes",
    "{} pats {}'s head and they blush LewdChamp",
    "{} pats {} NepComfy",
    "{} tries to pat {} but they move away KannaSpooks")
    
    bot.send_message(random.choice(responses).format(message.sender, target))
        
@bot.decorator('!commands')
def command_replycommands(message):
    bot.send_message('!sounds, !uptime, !pat <someone>, !remind <something> Daijoubu')
    
@bot.decorator('!love')
def command_love(message):
    if message.message:
        target = message.message[6:]
        if target:
            bot.send_message("There's {}% of love between {} and {} 💙".format(random.randrange(0, 100), message.sender, target))
    
def load_sounds():
    "This is a hacky way of adding functions into the bot's handling list"
    for key in sounds_json['global']:
        
        new = {'function': SFX(key['command'], key['path']).play_sound,
                'command': key['command'],
                'regexp': '',
                'access': 0}
        bot.handlers.append(new)

    print("Sounds loaded!")

if os.path.isfile("data/sounds.json"):
    sounds_json = load_json("data/sounds.json")
    load_sounds()

@bot.decorator('!remind')
def command_remind(message):
    with open('Chat reminders!.txt', 'a') as file:
        file.write("{}: {}\n".format(message.sender, message.message))

    bot.send_message("I'll remember to check it out PepoG")

@bot.decorator('!sounds')
def command_replysounds(message):
    message = ""

    sounds = list()
    for key in sounds_json['global']:
        sounds.append(key['command'])

    for sound in sorted(sounds):
        message += sound + ', '
        
    message = message[:-2] + ' KappaKappa'
    bot.send_message(message)

def load_greeetings():
    greets_json = load_json("data/users.json")
    """
    for key in users_json['users']:
        Greeter(key['username'], key['message'], key['sound'])
    """

end = timer()
print("loaded in {} seconds.".format(end-start))
print('----------------------------')
print('Now pooling...')
bot.pooling()
