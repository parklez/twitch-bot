import time
from parky_bot.models.message import Message
from parky_bot.utils.logger import get_logger, get_console_queue


LOGGER = get_logger()
CONSOLE = get_console_queue()


class ParkyBot:
    def __init__(self, irc, twitch=None):
        self.irc = irc
        self.twitch = twitch
        self.handlers = []
        self.chatters = []
        self.is_pooling = True
        self.twitch_init = False
        self.irc_init = False

    def pooling(self):
        if not self.irc.username:
            LOGGER.info('IRC username not set, stopping...')
            return

        if not self.twitch_init and self.twitch and self.twitch.channel:
            self.twitch_init = True
            self.twitch.connect()

        if not self.irc_init:
            self.irc_init = True
            self.irc.welcome()

        data = ''
        self.irc.irc_sock.setblocking(0)
        LOGGER.info('Now pooling...')

        while self.is_pooling:
            try:
                data = self.irc.irc_sock.recv(6144).decode('UTF-8')
            except (ConnectionAbortedError, OSError):
                try:
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    self.is_pooling = False
                    break
                continue
            except KeyboardInterrupt:
                self.is_pooling = False
                break

            if data == '':
                LOGGER.critical('IRC client received 0 bytes, stopping...')
                self.is_pooling = False
                break

            if data == 'PING :tmi.twitch.tv\r\n':
                self.irc.send_pong()
                LOGGER.debug('PONG')

            else:
                # BUG: If the sender decides to send '\n' midstring, their message will be split.
                for line in data.splitlines():
                    m = Message(line)
                    if m.sender:
                        LOGGER.debug(f'{m.sender}: {m.message}')
                        CONSOLE.put_nowait(m)
                    else:
                        LOGGER.debug(m.string)

                    if m.sender not in self.chatters and m.sender:
                        self.chatters.append(m.sender)
                    self.filter(m)

            data = ''
        LOGGER.info('Stopped pooling.')

    def filter(self, message: Message):
        """This method filters through the handlers, and calls its respective function.

        Args:
            message (Message): Message object.
        """
        for decorator in self.handlers:
            if (message.command in decorator['commands'] and decorator['active']
            and self.has_permission(decorator['access'], message)):
                decorator['function'](message)

    @staticmethod
    def has_permission(func_perm_level: int, message: Message) -> bool:
        """
        Checks permission based on hierarchy level

        0 - Viewer
        1 - Vip
        2 - Moderator
        3 - Broadcaster
        """
        if not func_perm_level:
            return True

        perms = {
            'broadcaster': 3,
            'moderator': 2,
            'vip': 1,
            '': 0
        }

        # Finding out the numerical equivalent for the permission
        user_perm = 0
        for perm in perms:
            if perm in message.badges:
                user_perm = perms[perm]
                break

        return user_perm >= func_perm_level

    def decorator(self, commands=[], regexp='', access=0):
        def wrapper(function):
            LOGGER.debug(f'Decorating: {function.__name__}')

            func = {
                'active': True,
                'function': function,
                'commands': commands,
                'regexp': regexp,
                'access': access
                }

            self.handlers.append(func)
            return function
        return wrapper

    def send_message(self, string):
        self.irc.send_message(string)
        m = Message('')
        m.message = string
        m.sender = self.irc.username
        CONSOLE.put_nowait(m)
