from parky_bot.settings import BOT
from parky_bot.models.message import Message


@BOT.decorator('!commands')
def command_replycommands(message: Message):
    BOT.send_message('!sounds, !uptime, !pat <someone>, !remind, !love <whom> <something> Daijoubu')


@BOT.decorator('!remind')
def command_remind(message: Message):
    with open('Chat reminders!.txt', 'a') as _file:
        _file.write("{}: {}\n".format(message.sender, message.message))
    BOT.send_message("I'll remember to check it out PepoG")
