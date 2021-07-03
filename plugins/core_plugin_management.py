from parky_bot.settings import BOT
from parky_bot.models.message import Message


@BOT.decorator(['!plugin'], access=3)
def command_toggle_plugin(message: Message):
    command = message.message.split()
    found = False

    if len(command) < 3:
        BOT.send_message('Syntax: !plugin <disable/enable> <!command>')
        return

    for decorator in BOT.handlers:
        # Finding out the responsible function
        # NOTE: Functions with a list of commands will be disabled altogether!
        if command[2] in decorator['commands']:
            found = True
            if command[1] == 'disable':
                decorator['active'] = False
                BOT.send_message(f'Command "{command[2]}" disabled!')
            elif command[1] == 'enable':
                decorator['active'] = True
                BOT.send_message(f'Command "{command[2]}" enabled!')
    if not found:
        BOT.send_message(f'Command {command[2]} not found. Did you forget a "!"?')
