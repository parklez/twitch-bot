import os
import sys
import threading
import random
import gtts
from parky_bot.twitch.irc import TwitchIRC
from parky_bot.twitch.api import TwitchAPI
from parky_bot.bot import ParkyBot
from parky_bot.models.sound import Sound
from parky_bot.models.message import Message
from parky_bot.utils.file_manager import load_json, create_settings_json


if getattr(sys, 'frozen', False):
    APP_PATH = os.path.dirname(sys.executable)
    RESOURCE_PATH = sys._MEIPASS
elif __file__:
    APP_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir)
    RESOURCE_PATH = os.path.join(os.path.dirname(__file__), 'resources')

SETTINGS_PATH = os.path.join(APP_PATH, 'settings.json')
SOUNDS_PATH = os.path.join(APP_PATH, 'sounds')

if not os.path.isfile(SETTINGS_PATH):
    create_settings_json(SETTINGS_PATH)
    print('You must write all your info under "settings.json" before continuing!')
    exit()

SETTINGS = load_json(SETTINGS_PATH)

IRC = TwitchIRC(SETTINGS['irc']['username'], SETTINGS['irc']['channel'], SETTINGS['irc']['token'])
API = TwitchAPI(SETTINGS['api']['client_id'], SETTINGS['api']['channel'], SETTINGS['api']['token'])
BOT = ParkyBot(API, IRC)
SOUNDS = []

# Adding custom chat functionality
print('----------------------------')

@BOT.decorator('!game')
def command_updategame(message: Message):
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
def command_updatestatus(message: Message):
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
def command_uptime(message: Message):
    time = BOT.twitch.get_uptime()
    if time:
        time = str(time)
        BOT.send_message(f'Stream has been live for: {time.split(".")[0]}')
    else:
        BOT.send_message('Stream is offline.')

@BOT.decorator('!pat')
def command_pat(message: Message):
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
        
    responses = ("{} gives {}'s head a soft pat Daijoubu",
    "{} WanISee // pat pat pat {}",
    "{} slowly strokes {}'s hair LoudDoge",
    "{} messes with {}'s hair PillowYes",
    "{} pats {}'s head and they blush LewdChamp",
    "{} pats {} NepComfy",
    "{} tries to pat {} but they move away KannaSpooks")

    BOT.send_message(random.choice(responses).format(message.sender, target))
        
@BOT.decorator('!commands')
def command_replycommands(message: Message):
    BOT.send_message('!sounds, !uptime, !pat <someone>, !remind, !love <whom> <something> Daijoubu')

@BOT.decorator('!love')
def command_love(message: Message):
    if message.message:
        target = message.message[6:]
        if target:
            BOT.send_message("There's {}% of love between {} and {} <3".format(random.randrange(0, 100), message.sender, target))

@BOT.decorator('!remind')
def command_remind(message: Message):
    with open('Chat reminders!.txt', 'a') as _file:
        _file.write("{}: {}\n".format(message.sender, message.message))
    BOT.send_message("I'll remember to check it out PepoG")

@BOT.decorator('!sounds')
def command_replysounds(message: Message):
    message = ""

    for sound in sorted(SOUNDS):
        message += sound + ', '
    message = message[:-2] + ' KappaKappa'
    BOT.send_message(message)

@BOT.decorator('!tts')
def command_replytts(message: Message):
    message = "!br \U0001F1E7\U0001F1F7, !au \U0001F1E6\U0001F1FA, !s !en \U0001F1EC\U0001F1E7, \
                !de \U0001F1E9\U0001F1EA, !es \U0001F1EA\U0001F1F8, !ja !jp \U0001F1EF\U0001F1F5, \
                !it \U0001F1EE\U0001F1F9, !pl \U0001F1F5\U0001F1F1, !pt \U0001F1F5\U0001F1F9, \
                !ru \U0001F1F7\U0001F1FA, !se \U0001F1F8\U0001F1EA, !uk \U0001F1FA\U0001F1E6, \
                !cn \U0001F1E8\U0001F1F3. Example: !fi nekubaka Honk"
    BOT.send_message(message)

for file in os.listdir(SOUNDS_PATH):
    if file.endswith(('.wav', '.mp3')):
        SOUNDS.append(file[:-4].lower())
        # Sound object is initialized when assigned to 's', avoiding parent variable search.
        # Don't: lambda m: Sound(os.path.join(SOUNDS_PATH, file)).play_sound(),
        #pylint: disable=cell-var-from-loop
        new = {'function': lambda m, s=Sound(os.path.join(SOUNDS_PATH, file)): s.play(),
                'command': f'!{file[:-4].lower()}',
                'regexp': '',
                'access': 0}
        BOT.handlers.append(new)
        print(f"Sound: {new['command']} created.")

@BOT.decorator(['!br', '!au', '!s', '!en', '!de', '!es', '!ja', '!jp', '!it', '!pl', '!pt',
                '!ru', '!se', '!uk', '!cn', '!fi'])
def command_gtts(message: Message):
    c = len(message.command)
    if not message.message[c:]:
        return

    langs = {'!br': 'pt-br', '!au': 'en-au', '!s': 'en-gb', '!en': 'en-gb', '!de': 'de',
            '!es': 'es-es', '!ja': 'ja', '!jp': 'ja', '!it': 'it', '!pl': 'pl',
            '!pt': 'pt-pt', '!ru': 'ru', '!se': 'sv', '!uk': 'uk', '!cn': 'zh-cn',
            '!fi': 'fi'}
    
    try:
        meme = gtts.gTTS(
            message.message[c:c+100],
            lang=langs[message.command])

        Sound(meme.get_urls()[0]).play()
    except AssertionError:
        pass

print('----------------------------')
sock_thread = threading.Thread(target=BOT.pooling)
sock_thread.start()

import tkinter
from PIL import Image, ImageTk


class ImageLabel(tkinter.Label):
    #https://stackoverflow.com/a/43770948
    """
    a label that displays images, and plays them if they are gifs
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0 # Current frame location
        self.frames = []

        try:
            i = 0
            while 1:
                frame = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self.frames.append(frame)
                im.seek(i)
                i += 1
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
BG_COLOR = '#212121'

APP = tkinter.Tk()

def on_closing():
    APP.destroy()
    BOT.is_pooling = False
    BOT.irc.disconnect()


APP.configure(background=BG_COLOR)
APP.title('parkybot')
APP.iconbitmap(os.path.join(RESOURCE_PATH, 'dog_pet_animal_japanese_shiba_inu_japan_icon_127300.ico')) # Bug: This breaks on linux
APP.minsize(250, 200)
APP.resizable(0, 0)
lbl = ImageLabel(APP, bg=BG_COLOR)
lbl.pack(padx=61, pady=25)
lbl.load(os.path.join(RESOURCE_PATH, 'YuukaGuitar.gif'))
tkinter.Label(APP, text='{parkybot}', font=('helvetica', 15), fg=FG_COLOR, bg=BG_COLOR).pack()
APP.protocol("WM_DELETE_WINDOW", on_closing)
APP.mainloop()
