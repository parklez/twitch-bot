import socket


class TwitchIRC:
    def __init__(self, username, channel, token):
        """
        IRC client with Twitch specific methods.
        Get your access token at www.twitchapps.com/tmi/
        """
        self.username = username
        self.token = token
        self.channel = '#' + channel
        self.host = 'irc.twitch.tv'
        self.port = 6667
        self.irc_sock = socket.socket()
        self.welcome()

    def welcome(self):
        """
        This function connects to twitch IRC in few steps:

        1. Connects to the server
        2. Sends a token
        3. Sends the username
        4. Joins a channel
        5. Requests extra tags (badges, emotes, etc)
        """
        self.irc_sock.connect((self.host, self.port))
        self.send_token()
        self.send_nick()
        self.join_channel()
        self.request_tags()

    def disconnect(self):
        self.irc_sock.close()

    def send(self, data):
        """
        This function converts data into bytes with UTF-8 encoding then socket.send()
        """
        self.irc_sock.send(bytes(data, 'UTF-8'))

    def send_pong(self):
        self.send("PONG :tmi.twitch.tv\r\n")

    def send_nick(self):
        self.send("NICK {}\r\n".format(self.username))

    def send_token(self):
        self.send("PASS {}\r\n".format(self.token))

    def join_channel(self):
        self.send("JOIN {}\r\n".format(self.channel))

    def part_channel(self):
        self.send("PART {}\r\n".format(self.channel))

    def send_message(self, message):
        self.send("PRIVMSG {} :{}\r\n".format(self.channel, message))

    def request_tags(self):
        #https://discuss.dev.twitch.tv/t/unable-to-register-for-irc-capabilities/27023
        self.send("CAP REQ :twitch.tv/tags\r\n")
