import os
from audioplayer import AudioPlayer
from parky_bot.utils.file_manager import make_dir
from parky_bot.settings import BOT, SOUNDS_PATH
from parky_bot.models.message import Message
from parky_bot.utils.logger import get_logger


logger = get_logger()

def scan_sounds_dir():
    SOUNDS = []
    if os.path.isdir(SOUNDS_PATH):
        for file in os.listdir(SOUNDS_PATH):
            if file.endswith(('.wav', '.mp3')):
                SOUNDS.append(file)
    else:
        make_dir(SOUNDS_PATH)
        return scan_sounds_dir()
    return SOUNDS

SOUNDS = scan_sounds_dir()
def create_sounds():
    for sound in SOUNDS:
        # Sound object is initialized when assigned to 's', avoiding parent variable search.
        # Don't: lambda m: Object.method(),
        #pylint: disable=cell-var-from-loop
        new = {'function': lambda _, s=AudioPlayer(os.path.join(SOUNDS_PATH, sound)): s.play(),
                'command': f'!{sound[:-4].lower()}',
                'regexp': '',
                'access': 0}
        BOT.handlers.append(new)
        logger.info(f"Sound: {new['command']} created.")
create_sounds()

@BOT.decorator('!sounds')
def command_replysounds(message: Message):
    message = ""

    for sound in sorted(SOUNDS):
        sound = sound[:-4].lower()
        message += sound + ', '
    message = message[:-2] + ' KappaKappa'
    BOT.send_message(message)
