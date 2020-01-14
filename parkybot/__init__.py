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
        
            
class ParkyBot:
    def __init__(self, twitch=None, irc=None):
        self.twitch = twitch
        self.irc = irc
        self.handlers = []
        self.chatters = []
        self.users = []
        self.is_pooling = True

    def pooling(self):
        if not self.irc:
            print("ParkyBot: IRC client not set!")
            return
        
        data = ""
        
        while self.is_pooling:
            # This socket is blocking
            data = self.irc.irc_sock.recv(1024).decode('UTF-8')
            
            if data == "PING :tmi.twitch.tv\r\n":
                self.irc.send_pong()
            
            else:
                m = Message(data)

                #print("{}: {}".format(m.sender, m.message))
                
                if m.sender not in self.chatters and m.sender:
                    self.chatters.append(m.sender)
                
                self.filter(m)
                
            data = ""
    
    def filter(self, message: Message):
        'Tests each filter on the Message object'
        for decorator in self.handlers:
            if decorator['command'] == message.command:
                decorator['function'](message)
        """
        for user in self.users:
            if m.sender == user['username']:
                self.send_message(user['message'])
                user['sound']
        """
        
    def decorator(self, command='', regexp='', access=0):
        def wrapper(function):
            print('Decorating: {}'.format(function.__name__))
            
            new = {'function': function,
                   'command': command,
                   'regexp': regexp,
                   'access': access}
            self.handlers.append(new)
            return function
        return wrapper

    def send_message(self, string):
        self.irc.send_message(string)
        
