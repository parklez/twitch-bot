import socket
from parky_bot.utils.logger import get_logger


LOGGER = get_logger()


class TwitchIRC:
    def __init__(self, username: str, channel: str, token: str):
        """Class to interact with Twitch's IRC using a socket.

        Args:
            username (str): Username to join a channel as
            channel (str): Channel to join
            token (str): Token for chat access (generated at www.twitchapps.com/tmi/)
        """

        self.username = username
        self.token = token
        self.channel = '#' + channel
        self.host = 'irc.twitch.tv'
        self.port = 6667
        self.irc_sock = socket.socket()

        #self.welcome()

    def reconnect(self):
        self.disconnect()
        self.welcome()

    def welcome(self):
        """Connects to twitch IRC in few steps:

        1. Connects to the server
        2. Requests extra tags (badges, emotes, etc)
        3. Sends a token
        4. Sends the username
        5. Joins a channel
        """

        self.irc_sock = socket.socket()
        self.irc_sock.connect((self.host, self.port))
        self.request_tags()
        #self.request_membership()
        #self.request_commands()
        self.send_token()
        self.send_nick()
        self.join_channel()

    def disconnect(self):
        self.irc_sock.close()

    def send(self, data: str) -> bool:
        """Converts data into bytes with UTF-8 encoding then socket.send()"""
        try:
            self.irc_sock.send(bytes(data, 'UTF-8'))
            return True
        except Exception as err:
            LOGGER.error(err)
            return False

    def send_pong(self):
        self.send('PONG :tmi.twitch.tv\r\n')

    def send_nick(self):
        self.send(f'NICK {self.username}\r\n')

    def send_token(self):
        self.send(f'PASS {self.token}\r\n')

    def join_channel(self):
        self.send(f'JOIN {self.channel}\r\n')

    def part_channel(self):
        self.send(f'PART {self.channel}\r\n')

    def send_message(self, message):
        self.send(f'PRIVMSG {self.channel} :{message}\r\n')

    def request_tags(self):
        # https://discuss.dev.twitch.tv/t/unable-to-register-for-irc-capabilities/27023
        self.send('CAP REQ :twitch.tv/tags\r\n')

    def request_membership(self):
        self.send('CAP REQ :twitch.tv/membership\r\n')

    def request_commands(self):
        self.send('CAP REQ :twitch.tv/commands\r\n')
