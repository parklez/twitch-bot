import re


class Message:
    def __init__(self, string):
        self.string = string
        self.message = ''
        self.sender = ''
        self.targets = []
        self.command = None
        
        self._parse(self.string)

    def _parse(self, string):
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
