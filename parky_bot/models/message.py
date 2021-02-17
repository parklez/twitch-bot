import re


class Message:

    def __init__(self, string):
        """Message object contains several atributes from Twitch's IRC string,
        such as:
            * string (str): IRC string.
            * message (str): Sender's message.
            * sender (str): Sender's username.
            * channel (str): Channel.
            * tags (dict): dict of available user tags (if tags are enabled).
            * badges (dict): dict of available badges like broadcaster, vip (if tags are enabled).
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
        self.tags = {}
        self.badges = {}
        self.targets = []
        self.command = ''

        self.parse()

    def parse(self):
        if "PRIVMSG" not in self.string.split():
            return

        if self.string.startswith('@'):
            regex = r'@(.*) :(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)'
            (tags,
            self.sender,
            self.channel,
            self.message) = re.search(regex, self.string).groups()

            tags = tags.split(';')
            self.tags = dict([tag.split('=') for tag in tags])

            badges = self.tags.get('badges')
            if badges:
                self.badges = dict([badge.split('/') for badge in badges.split(',')])

        else:
            regex = r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)'
            (self.sender,
            self.channel,
            self.message) = re.search(regex, self.string).groups()

        self.sender = self.tags.get('display-name', self.sender)

        words = self.message.split()

        self.command = words[0].lower()

        for word in words:
            if word.startswith("@"):
                self.targets.append(word.strip("@"))
