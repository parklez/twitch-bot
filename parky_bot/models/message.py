import re


class Message:
    def __init__(self, string):
        self.string = string
        self.message = ''
        self.sender = ''
        self.badges = dict()
        self.targets = []
        self.command = None
        
        self.new_parser()

    def simple_parser(self):
        """Splits sender, message and target(s)
        and returns attributes"""
    
        # Sender and Message string
        if not self.string:
            return

        if self.string.split(' ')[1] == 'PRIVMSG':
            self.sender = re.search(r"\w+", self.string).group(0)
            self.message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :").sub("", self.string).rstrip('\n').rstrip()
            
        if self.message.startswith("!"):
            self.command = self.message.lower().split()[0]
            
        words = self.message.split(" ")
        
        for word in words:
            if word.startswith("@"):
                self.targets.append(word.strip("@"))

    def new_parser(self):
        if self.string.split()[2] != "PRIVMSG":
            return

        self.message = re.search(r'PRIVMSG #\w+ :(.*)', self.string).group(1)
        
        string = self.string.split()
        badges = string[0].split(';')
        for item in badges:
            item = item.split('=')
            self.badges[item[0]] = item[1]
        print(self.badges)
        
        self.sender = self.badges.get('display-name')

        if self.message.startswith("!"):
            self.command = self.message.lower().split()[0]

        words = self.message.split(" ")
        for word in words:
            if word.startswith("@"):
                self.targets.append(word.strip("@"))
