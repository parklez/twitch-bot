import os
import queue
import time
from datetime import datetime
import threading
from audioplayer import AudioPlayer
import gtts
from parky_bot.settings import BOT, APP_PATH, SETTINGS
from parky_bot.models.message import Message
from parky_bot.utils.logger import get_logger
from parky_bot.utils.file_manager import make_dir


LOGGER = get_logger()
TEMP_DIR = os.path.join(APP_PATH, 'sounds', 'gtts')
QUEUE = queue.Queue()


@BOT.decorator(['!tts'])
def command_replytts(message: Message):
    message = "!br \U0001F1E7\U0001F1F7, !au \U0001F1E6\U0001F1FA, !s !en \U0001F1EC\U0001F1E7, " \
              "!us \U0001F1FA\U0001F1F8, !de \U0001F1E9\U0001F1EA, !es \U0001F1EA\U0001F1F8, " \
              "!it \U0001F1EE\U0001F1F9, !pl \U0001F1F5\U0001F1F1, !pt \U0001F1F5\U0001F1F9, " \
              "!ru \U0001F1F7\U0001F1FA, !se \U0001F1F8\U0001F1EA, !uk \U0001F1FA\U0001F1E6, " \
              "!cn \U0001F1E8\U0001F1F3, !ja !jp \U0001F1EF\U0001F1F5, !fr \U0001F1EB\U0001F1F7. " \
              "Example: !fr animé milkers Honk"
    BOT.send_message(message)

@BOT.decorator(['!br', '!au', '!s', '!en', '!de', '!es', '!ja', '!jp', '!it', '!pl', '!pt',
                '!ru', '!se', '!uk', '!cn', '!fi', '!fr', '!us'])
def command_gtts(message: Message):
    size = len(message.command)
    if not message.message[size:]:
        return

    langs = {'!br': 'pt-br', '!au': 'en-au', '!s': 'en-gb', '!en': 'en-gb', '!de': 'de',
            '!es': 'es-es', '!ja': 'ja', '!jp': 'ja', '!it': 'it', '!pl': 'pl',
            '!pt': 'pt-pt', '!ru': 'ru', '!se': 'sv', '!uk': 'uk', '!cn': 'zh-cn',
            '!fi': 'fi', '!fr': 'fr', '!us': 'en-us'}

    result = gtts.gTTS(
        message.message[size:size+100],
        lang=langs[message.command])

    QUEUE.put_nowait(result)

def gtts_daemon():
    while BOT.is_pooling:
        try:
            response = QUEUE.get(block=False) # This blocks and hangs the program entirely
            file_name = os.path.join(TEMP_DIR, f'gtts_{datetime.now().microsecond}.mp3')
            response.save(file_name)
            sound = AudioPlayer(file_name)
            sound.volume = SETTINGS.get('volume', 100)
            sound.play(block=True)
            os.remove(file_name)
            QUEUE.task_done()
        except queue.Empty:
            pass # Ignore and try again later
        except Exception as err:
            os.remove(file_name)
            LOGGER.error(err, exc_info=True)
        time.sleep(1) # Lessen the CPU impact.

make_dir(TEMP_DIR)
threading.Thread(target=gtts_daemon).start()
