from parky_bot.settings import BOT
from parky_bot.models.message import Message


@BOT.decorator(['!game'])
def command_updategame(message: Message):
    prefix = len(message.command) + 1
    if not message.message[prefix:]:
        return BOT.send_message(f'Currently playing: "{BOT.twitch.game}"')

    if 'broadcaster' in message.badges:
        result = BOT.twitch.update_stream(game_title=message.message[prefix:])
        if result:
            BOT.send_message(f'Game set to: "{BOT.twitch.game}"')
        else:
            BOT.send_message(f'Twitch API failed to update game!')

@BOT.decorator(['!status', '!title'])
def command_updatestatus(message: Message):
    prefix = len(message.command) + 1
    if not message.message[prefix:]:
        return BOT.send_message(f'Status: "{BOT.twitch.status}"')

    if 'broadcaster' in message.badges:
        result = BOT.twitch.update_stream(stream_title=message.message[prefix:])
        if result:
            BOT.send_message(f'Title set to: "{BOT.twitch.status}"')
        else:
            BOT.send_message(f'Twitch API failed to update status!')

@BOT.decorator(['!uptime'])
def command_uptime(message: Message):
    time = BOT.twitch.get_uptime()
    if not time:
        return BOT.send_message(f'{BOT.twitch.channel} is offline.')

    time = str(time).split('.')[0]
    time = time.replace(':', ' hour(s), ', 1)
    time = time.replace(':', ' minutes, ')
    time += ' seconds.'
    time = time.replace('0 hour(s), ', '') # Removing this case.

    BOT.send_message(f'{BOT.twitch.channel} has been live for {time}')
