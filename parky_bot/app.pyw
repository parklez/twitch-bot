from parky_bot.settings import SETTINGS, SOUNDS_PATH
from parky_bot.twitch.irc import TwitchIRC
from parky_bot.twitch.api import TwitchAPI
from parky_bot.models.sfx_and_greetings import SFX, VOLUME
from parky_bot.bot import ParkyBot


IRC = TwitchIRC(SETTINGS['irc']['username'], SETTINGS['irc']['channel'], SETTINGS['irc']['token'])
API = TwitchAPI(SETTINGS['api']['client_id'], SETTINGS['api']['channel'], SETTINGS['api']['token'])
BOT = ParkyBot(API, IRC)
SOUNDS = dict()

# Adding custom chat functionality
print('----------------------------')
import os
import random
import gtts
import vlc


@BOT.decorator('!game')
def command_updategame(message):
    if message.message[6:]:
        if 'broadcaster' in message.badges.get('badges'):
            result = BOT.twitch.update_game(message.message[6:])
            if result.ok:
                BOT.send_message(f'Game set to: "{BOT.twitch.game}"')
            else:
                BOT.send_message(f'{result.text}')
    else:
        BOT.send_message(f'Currently playing: "{BOT.twitch.game}"')

@BOT.decorator('!status')
def command_updatestatus(message):
    if message.message[8:]:
        if 'broadcaster' in message.badges.get('badges'):
            result = BOT.twitch.update_status(message.message[8:])
            if result.ok:
                BOT.send_message(f'Status set to: "{BOT.twitch.status}"')
            else:
                BOT.send_message(f'{result.text}')
    else:
        BOT.send_message(f'Status: "{BOT.twitch.status}"')

@BOT.decorator('!uptime')
def command_uptime(message):
    time = BOT.twitch.get_uptime()
    if time:
        time = str(time)
        BOT.send_message(f'Stream has been live for: {time.split(".")[0]}')
    else:
        BOT.send_message('Stream is offline.')

@BOT.decorator('!pat')
def command_pat(message):
    print(message.targets)
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
    
    """
    if target.lower() == message.sender.lower():
        BOT.send_message("WanISee // {} pat pat pat".format(message.sender))
        return
    """
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
    BOT.send_message('!sounds, !uptime, !pat <someone>, !remind, !love <whom> <something> Daijoubu')
    
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


for file in os.listdir(SOUNDS_PATH):
    if file.endswith(('.wav', '.mp3')):
        print(file)
        new = {'function': SFX(os.path.join(SOUNDS_PATH, file)).play_sound,
                'command': '!' + file[:-4].lower(),
                'regexp': '',
                'access': 0}
        BOT.handlers.append(new)
print("Sounds loaded!")


@BOT.decorator([
    '!s', '!br', '!af', '!ar', '!bn', '!bs', '!ca', '!cs', '!cy', '!da', '!de', '!el', '!en-au',
    '!en-ca', '!en-gb', '!en-gh', '!en-ie', '!en-in', '!en-ng', '!en-nz', '!en-ph', '!en-tz',
    '!en-uk', '!en-us', '!en-za', '!en', '!eo', '!es-es', '!es-us', '!es', '!et', '!fi', '!fr-ca',
    '!fr-fr', '!fr', '!gu', '!hi', '!hr', '!hu', '!hy', '!id', '!is', '!it', '!ja', '!jw',
    '!km', '!kn', '!ko', '!la', '!lv', '!mk', '!ml', '!mr', '!my', '!ne', '!nl', '!no', '!pl',
    '!pt-br', '!pt-pt', '!pt', '!ro', '!ru', '!si', '!sk', '!sq', '!sr', '!su', '!sv', '!sw',
    '!ta', '!te', '!th', '!tl', '!tr', '!uk', '!ur', '!vi', '!zh-cn', '!zh-tw'
    ])
def command_gtts(message):
    if not message.message[len(message.command):]:
        return

    if message.command == '!s':
        message.command = '!en'
    elif message.command == '!br':
        message.command = '!pt-br'
    
    try:
        meme = gtts.gTTS(message.message[3:103], lang=message.command[1:])
        audio = vlc.MediaPlayer(meme.get_urls()[0])
        audio.audio_set_volume(VOLUME)
        audio.play()
    except AssertionError:
        return

print('----------------------------')
print('Now pooling...')
import threading
sock_thread = threading.Thread(target=BOT.pooling)
sock_thread.start()

import tkinter
from PIL import Image, ImageTk
from itertools import count

class ImageLabel(tkinter.Label):
    #https://stackoverflow.com/a/43770948
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                frame = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self.frames.append(frame)
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

FG_COLOR = '#D6F0DA'
BG_COLOR = '#303030'

APP = tkinter.Tk()

def on_closing():
    APP.destroy()
    IRC.disconnect()

APP.configure(background=BG_COLOR)
APP.title('parkybot')
APP.minsize(250, 200)
APP.resizable(0, 0)
"""
image = Image.open('parky_bot/resources/parkpy2.png')
image = image.resize((128, 128), resample=3)
logo_file = ImageTk.PhotoImage(image)
logo = tkinter.Label(image=logo_file, bg=BG_COLOR)
logo.image = logo_file
logo.pack()
"""
lbl = ImageLabel(APP, bg=BG_COLOR, pady=20)
lbl.pack()
lbl.load('parky_bot/resources/barkychan128.gif')
tkinter.Label(APP, text='{8d112dc}', font=('helvetica', 15), fg=FG_COLOR, bg=BG_COLOR).pack()
APP.protocol("WM_DELETE_WINDOW", on_closing)
APP.mainloop()
