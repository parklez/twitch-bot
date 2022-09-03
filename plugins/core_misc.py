from parky_bot.settings import BOT
from parky_bot.models.message import Message


@BOT.decorator(['!commands'])
def command_replycommands(_: Message):
    BOT.send_message('!sounds, !tts, !uptime, !pat <someone>,' +
                     ' !remind <something>, !love <whom> <something>.')


@BOT.decorator(['!remind'])
def command_remind(message: Message):
    with open('CHAT REMINDERS!.txt', 'a') as _file:
        _file.write(f'{message.sender}: {message.message}\n')
    BOT.send_message('I\'ll remember to check it out!')
