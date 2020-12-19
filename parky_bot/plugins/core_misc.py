from parky_bot.settings import BOT
from parky_bot.models.message import Message


@BOT.decorator(['!commands'])
def command_replycommands(message: Message):
    BOT.send_message(
        '!sounds, !tts, !uptime, !pat <someone>, !remind <something>, !love <whom> <something>.')

@BOT.decorator(['!remind'])
def command_remind(message: Message):
    with open('Chat reminders!.txt', 'a') as _file:
        _file.write("{}: {}\n".format(message.sender, message.message))
    BOT.send_message("I'll remember to check it out!")
