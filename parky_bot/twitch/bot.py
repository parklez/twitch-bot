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
        self.irc_connected_successfully = False

    def connect_to_twitch(self):
        if not self.twitch_init and self.twitch and self.twitch.channel:
            LOGGER.debug('Initializing Twitch API connection...')
            self.twitch_init = True
            self.twitch.connect()

    def connect_to_chat(self):
        if not self.irc.username:
            LOGGER.info('IRC username not set, stopping...')
            self.is_pooling = False
            return

        if not self.irc_init:
            LOGGER.debug('Initializing chat connection...')
            self.irc_init = True
            self.irc.welcome()

    def pooling(self):
        self.connect_to_twitch()
        self.connect_to_chat()
        data = ''
        LOGGER.debug('Attemping to receive message from chat...')

        while self.is_pooling:
            try:
                data = self.irc.irc_sock.recv(6144).decode('UTF-8')
                if not self.irc_connected_successfully:
                    self.irc_connected_successfully = True
                    LOGGER.info('Connected to chat - GLHF!')
            except (ConnectionAbortedError, OSError):
                if not self.is_pooling:
                    break
                LOGGER.error('Connection aborted... re-connecting in 3 seconds...')
                time.sleep(3)
                self.irc_connected_successfully = False
                self.irc.reconnect()
                continue
            except KeyboardInterrupt:
                self.is_pooling = False
                return

            if data == '':
                LOGGER.error('Received 0 bytes from chat, re-connecting in 3 seconds...')
                time.sleep(3)
                self.irc_connected_successfully = False
                self.irc.reconnect()
                continue

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
            time.sleep(0.1)

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
