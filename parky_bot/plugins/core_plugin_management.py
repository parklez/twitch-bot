from parky_bot.settings import BOT
from parky_bot.models.message import Message


@BOT.decorator('!plugin')
def command_toggle_plugin(message: Message):
    if 'broadcaster' in message.badges.get('badges', ''):
        command = message.message.split()
        found = False
        if len(command) > 2:
            for decorator in BOT.handlers:
                # Finding out the responsible function
                # NOTE: Functions with a list of commands will be disabled altogether!
                if ((isinstance(decorator['command'], str)
                    and command[2] == decorator['command'])
                or ((isinstance(decorator['command'], list)
                    and command[2] in decorator['command']))):
                    found = True
                    if command[1] == 'disable':
                        decorator['active'] = False
                        BOT.send_message(f'Command "{command[2]}" disabled!')
                    elif command[1] == 'enable':
                        decorator['active'] = True
                        BOT.send_message(f'Command "{command[2]}" enabled!')
            if not found:
                BOT.send_message(f'Command {command[2]} not found. Did you forget a "!"?')
        else:
            BOT.send_message('Syntax: !plugin <disable/enable> <!command>')
