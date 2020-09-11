from parky_bot.settings import SETTINGS, SOUNDS
from parky_bot.twitch_api.twitch import TwitchIRC, TwitchAPI
from parky_bot.bot import ParkyBot
from parky_bot.sfx_and_greetings import SFX, VOLUME


IRC = TwitchIRC(SETTINGS['irc']['username'], SETTINGS['irc']['channel'], SETTINGS['irc']['token'])
API = TwitchAPI(SETTINGS['api']['client_id'], SETTINGS['api']['channel'], SETTINGS['api']['token'])
BOT = ParkyBot(API, IRC)

# Adding custom chat functionality
print('----------------------------')
import random

@BOT.decorator('!game')
def command_updategame(message):
    if 'broadcaster' in message.badges.get('badges'):
        BOT.twitch.update_game(message.message[6:])
        BOT.send_message("We're now playing: {}".format(BOT.twitch.last_call))

@BOT.decorator('!status')
def command_updatestatus(message):
    if 'broadcaster' in message.badges.get('badges'):
        BOT.twitch.update_status(message.message[8:])
        BOT.send_message("Stream title: {}".format(BOT.twitch.last_call))

@BOT.decorator('!uptime')
def command_uptime(message):
    time = BOT.twitch.get_uptime()
    BOT.send_message(time)

@BOT.decorator('!pat')
def command_pat(message):
    if not message.targets:
        target = message.message[5:]
        if not target:
            return
    else:
        target = message.targets[0]
    
    if target.lower() == BOT.irc.username.lower():
        doggos = ('dogeWink', 'dogeKek', 'Wowee', 'WooferWhat')
        BOT.send_message(random.choice(doggos))
        return
        
    if target.lower() == message.sender.lower():
        BOT.send_message("WanISee // {} pat pat pat".format(message.sender))
        return
        
    responses = ("{} gives {}'s head a soft pat Daijoubu",
    "{} WanISee // pat pat pat {}",
    "{} slowly strokes {}'s hair LoudDoge",
    "{} messes with {}'s hair PillowYes",
    "{} pats {}'s head and they blush LewdChamp",
    "{} pats {} NepComfy",
    "{} tries to pat {} but they move away KannaSpooks")
    
    BOT.send_message(random.choice(responses).format(message.sender, target))
        
@BOT.decorator('!commands')
def command_replycommands(message):
    BOT.send_message('!sounds, !uptime, !pat <someone>, !remind <something> Daijoubu')
    
@BOT.decorator('!love')
def command_love(message):
    if message.message:
        target = message.message[6:]
        if target:
            BOT.send_message("There's {}% of love between {} and {} <3".format(random.randrange(0, 100), message.sender, target))

@BOT.decorator('!remind')
def command_remind(message):
    with open('Chat reminders!.txt', 'a') as file:
        file.write("{}: {}\n".format(message.sender, message.message))

    BOT.send_message("I'll remember to check it out PepoG")

@BOT.decorator('!sounds')
def command_replysounds(message):
    message = ""

    sounds = list()
    for key in SOUNDS['global']:
        sounds.append(key['command'])

    for sound in sorted(sounds):
        message += sound + ', '
        
    message = message[:-2] + ' KappaKappa'
    BOT.send_message(message)

def load_greeetings():
    pass
    #greets_json = load_json("data/users.json")
    """
    for key in users_json['users']:
        Greeter(key['username'], key['message'], key['sound'])
    """

def load_sounds():
    "This is a hacky way of adding functions into the bot's handling list"
    for key in SOUNDS['global']:
        new = {'function': SFX(key['path']).play_sound,
                'command': key['command'],
                'regexp': '',
                'access': 0}
        BOT.handlers.append(new)
    print("Sounds loaded!")
load_sounds()

@BOT.decorator('!s')
def command_gtts(message):
    #Need to find a way to play this audio from the memory directly.
    import gtts
    import vlc
    if not message.message[3:]:
        return
    meme = gtts.gTTS(message.message[3:])
    meme.save('tts_temp.mp3')
    audio = vlc.MediaPlayer('tts_temp.mp3')
    audio.audio_set_volume(VOLUME)
    audio.play()

print('----------------------------')
print('Now pooling...')
BOT.pooling()
