from parky_bot.settings import BOT
from parky_bot.models.message import Message


@BOT.decorator(['!game'])
def command_updategame(message: Message):
    prefix = len(message.command) + 1
    if message.message[prefix:]:
        if 'broadcaster' in message.badges.get('badges'):
            result = BOT.twitch.update_game(message.message[prefix:])
            if result.ok:
                BOT.send_message(f'Game set to: "{BOT.twitch.game}"')
            else:
                BOT.send_message(f'{result.text}')
    else:
        BOT.send_message(f'Currently playing: "{BOT.twitch.game}"')

@BOT.decorator(['!status', '!title'])
def command_updatestatus(message: Message):
    prefix = len(message.command) + 1
    if message.message[prefix:]:
        if 'broadcaster' in message.badges.get('badges'):
            result = BOT.twitch.update_status(message.message[prefix:])
            if result.ok:
                BOT.send_message(f'Status set to: "{BOT.twitch.status}"')
            else:
                BOT.send_message(f'{result.text}')
    else:
        BOT.send_message(f'Status: "{BOT.twitch.status}"')

@BOT.decorator(['!uptime'])
def command_uptime(message: Message):
    time = BOT.twitch.get_uptime()
    if time:
        time = str(time)
        BOT.send_message(f'Stream has been live for: {time.split(".")[0]}')
    else:
        BOT.send_message('Stream is offline.')
