import time
from parky_bot.models.message import Message
from parky_bot.utils.logger import get_logger, get_console_queue


LOGGER = get_logger()
CONSOLE = get_console_queue()


class ParkyBot:
    def __init__(self, irc, twitch):
        self.irc = irc
        self.twitch = twitch
        self.handlers = []
        self.chatters = []
        self._pooling = False
        self.alive = False
        self.irc_connected_successfully = False

    def connect_to_twitch(self):
        if self.twitch and self.twitch.token and self.twitch.client_id:
            LOGGER.debug('Initializing Twitch API...')
            self.twitch.connect()

    def connect_to_chat(self) -> bool:
        if not self.irc.username or not self.irc.channel[1:] or not self.irc.token:
            LOGGER.debug('IRC settings not fully set, stopping...')
            self._pooling = False
            return

        LOGGER.info('Connecting to chat...')
        self.irc.welcome()
        self._pooling = True
        return True

    def pooling(self):
        self.connect_to_twitch()
        if not self.connect_to_chat():
            return

        data = ''
        LOGGER.debug('Attemping to receive message from chat...')
        self.alive = True

        while self._pooling:
            try:
                data = self.irc.irc_sock.recv(6144).decode('UTF-8')
                if not self.irc_connected_successfully:
                    self.irc_connected_successfully = True
                    LOGGER.info('Connected to %s - GLHF!', self.irc.channel)
            except (ConnectionAbortedError, OSError):
                if not self._pooling:
                    break
                LOGGER.error('Connection aborted... re-connecting in 3 seconds...')
                self.reconnect()
                continue
            except KeyboardInterrupt:
                self._pooling = False
                return

            if data == '':
                LOGGER.error('Received 0 bytes from chat, re-connecting in 3 seconds...')
                self.reconnect()
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

        self.alive = False
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
        # This is only necessary if the IRC user is not the owner of the channel(?)
        if self.irc.username != self.twitch.channel:
            m = Message('')
            m.message = string
            m.sender = self.irc.username
            CONSOLE.put_nowait(m)

    def disconnect(self):
        self._pooling = False
        self.irc_connected_successfully = False
        self.irc.disconnect()
        # Wait until pooling is over before moving on
        while self.alive:
            pass

    def reconnect(self):
        time.sleep(3)
        self.irc_connected_successfully = False
        self.irc.reconnect()
