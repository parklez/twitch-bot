import random
from parky_bot.settings import BOT
from parky_bot.models.message import Message


RESPONSES  = ('{} gives {}\'s head a soft pat Daijoubu',
              '{} WanISee // pat pat pat {}',
              '{} slowly strokes {}\'s hair LoudDoge',
              '{} messes with {}\'s hair PillowYes',
              '{} pats {}\'s head and they blush LewdChamp',
              '{} pats {} NepComfy',
              '{} tries to pat {} but they move away KannaSpooks')


@BOT.decorator(['!pat'])
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

    BOT.send_message(random.choice(RESPONSES).format(message.sender, target))

@BOT.decorator(['!love'])
def command_love(message: Message):
    if message.message:
        target = message.message[6:]
        if target:
            BOT.send_message(f'There\'s {random.randrange(0, 100)}% of love between ' +
                             f'{message.sender} and {target} <3')
