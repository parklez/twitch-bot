from parky_bot.settings import BOT
from parky_bot.models.message import Message
from parky_bot.utils.file_manager import create_json, load_json


CUSTOM_RESPONSES_FILE = 'my_custom_commands.json'


def save_response_file(command: dict, file=CUSTOM_RESPONSES_FILE) -> str:
    loaded_list = []
    try:
        loaded_list = load_json(file)
    except FileNotFoundError:
        pass
    preexisting = 'added'
    for stored_command in loaded_list:
        if stored_command['command'] == command['command']:
            loaded_list.remove(stored_command)
            preexisting = 'updated'
            break

    loaded_list.append(command)
    create_json(loaded_list, file)
    return preexisting


def create_responses_from_file(file=CUSTOM_RESPONSES_FILE):
    """Load json file cotaining a list of dicts, representing
    a command object.

    Args:
        file (str, optional): JSON file with commands.
        Defaults to 'my_custom_commands.json'.
    """
    try:
        custom_commands = load_json(file)
        for custom_command in custom_commands:
            # TODO: Figure out why arguments can't be directly written
            # under the function's instructions. - I assume that
            # for every iteration, the function code is overwritten,
            # and only the arguments are being correctly saved by the
            # decorator.
            @BOT.decorator([custom_command['command']])
            def custom_function(_, r=custom_command['response']):
                # My theory can be "proven" by checking this:
                #print(custom_command['command'], id(custom_command['command']))
                BOT.send_message(r)
    except FileNotFoundError:
        return


def erase_response_from_file(trigger: str, file=CUSTOM_RESPONSES_FILE) -> bool:
    loaded_list = load_json(file)
    for command in loaded_list:
        if command['command'] == trigger:
            loaded_list.remove(command)
            create_json(loaded_list, file)

            return True
    return False


@BOT.decorator(['!add'], access=1)
def command_add_custom_responses(message: Message):
    """Decorates a new function while saving them.

    Args:
        message (Message): !add <command> <response>
    """
    # TODO
    # Save entire function as-is, so that some data can be persistent,
    # such as counters or whatever.
    commands = message.message.split()
    m = message.message

    if len(commands) < 3:
        BOT.send_message('Syntax: !add <command> <text response>')
        return

    command = commands[1].lower()
    response = m[len(commands[0])+len(commands[1])+2:]

    # https://www.codementor.io/@arpitbhayani/overload-functions-in-python-13e32ahzqt
    # When overloading the same name, a new function is created entirely. check id().
    # Python will not loose its memory address since it's being referenced elsewhere.
    @BOT.decorator([command])
    def custom_function(_):
        BOT.send_message(response)

    result = save_response_file({'command': command, 'response': response})
    BOT.send_message(f'"{command}" {result}! \U0001F4BE')


@BOT.decorator(['!remove', '!erase', '!del'], access=1)
def command_remove_custom_responses(message: Message):
    commands = message.message.split()
    if len(commands) < 2:
        BOT.send_message('Syntax: !remove <!command>')
        return
    result = erase_response_from_file(commands[1])

    for handler in BOT.handlers:
        if commands[1] in handler['commands']:
            BOT.handlers.remove(handler)

    BOT.send_message(f'{commands[1]} {"deleted!" if result else "not found!"}')


create_responses_from_file()
