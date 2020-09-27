import re


class Message:

    def __init__(self, string):
        self.string = string
        self.message = ''
        self.sender = ''
        self.badges = dict()
        self.targets = []
        self.command = None
        
        self.parser()

    def parser(self):
        if "PRIVMSG" not in self.string.split():
            return

        self.message = re.search(r'PRIVMSG #\w+ :(.*)', self.string).group(1).rstrip()
        
        string = self.string.split()
        badges = string[0].split(';')
        for item in badges:
            item = item.split('=')
            try:
                self.badges[item[0]] = item[1]
            except Exception:
                pass
        
        self.sender = self.badges.get('display-name')
        
        if self.message.startswith("!"):
            self.command = self.message.lower().split()[0]

        words = self.message.split(" ")
        for word in words:
            if word.startswith("@"):
                self.targets.append(word.strip("@"))
