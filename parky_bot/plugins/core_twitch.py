from parky_bot.settings import BOT
from parky_bot.models.message import Message


@BOT.decorator(['!game'])
def command_updategame(message: Message):
    prefix = len(message.command) + 1
    if message.message[prefix:]:
        if 'broadcaster' in message.badges:
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
        if 'broadcaster' in message.badges:
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
    if not time:
        time = str(time).split('.')[0]
        time = time.replace(':', ' hours, ')
        time = time.replace(':', ' minutes, ')
        time += ' seconds.'
        time = time.replace('0 hour(s), ', '') # Removing this case.

        BOT.send_message(f'{BOT.twitch.channel} has been live for {time}')
    else:
        BOT.send_message(f'{BOT.twitch.channel} is offline.')
