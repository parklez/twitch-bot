import re


class Message:

    def __init__(self, string):
        """Message object contains several atributes from Twitch's IRC string,
        such as:
            * string (str): IRC string.
            * message (str): Sender's message.
            * sender (str): Sender's username.
            * channel (str): Channel.
            * badges (dict): dict of available user badges (if tags are enabled).
                To learn more: https://dev.twitch.tv/docs/irc/tags#privmsg-twitch-tags
            * targets (list): list of tagged usernames in the message starting with "@".
            * command (str): First word of the message.
        Args:
            string (str): IRC string.
        """

        self.string = string
        self.message = ''
        self.sender = ''
        self.channel = ''
        self.badges = {}
        self.targets = []
        self.command = ''

        self.parse()

    def parse(self):
        if "PRIVMSG" not in self.string.split():
            return

        if self.string.startswith('@'):
            regex = r'@(.*) :(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)'
            (badges,
            self.sender,
            self.channel,
            self.message) = re.search(regex, self.string).groups()

            for item in badges.split(';'):
                item = item.split('=')
                try:
                    self.badges[item[0]] = item[1]
                except IndexError:
                    pass
        else:
            regex = r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)'
            (self.sender,
            self.channel,
            self.message) = re.search(regex, self.string).groups()

        self.sender = self.badges.get('display-name', self.sender)

        words = self.message.split()

        self.command = words[0].lower()

        for word in words:
            if word.startswith("@"):
                self.targets.append(word.strip("@"))
