import time
from parky_bot.models.message import Message


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
        self.irc.irc_sock.setblocking(0)
        
        while self.is_pooling:
            try:
                data = self.irc.irc_sock.recv(1024).decode('UTF-8')
            except (ConnectionAbortedError, OSError):
                time.sleep(0.05)
                continue

            if data == "PING :tmi.twitch.tv\r\n":
                self.irc.send_pong()
            
            else:
                # BUG: If 'data' contains two or more lines (when people spam), this will crash:
                m = Message(data)
                
                if m.sender not in self.chatters and m.sender:
                    self.chatters.append(m.sender)
                
                self._filter(m)
                
            data = ""
        print('Stopped pooling.')
    
    def _filter(self, message: Message):
        'Tests each filter on the Message object'
        for decorator in self.handlers:
            if type(decorator['command']) == str:
                if message.command == decorator['command']:
                    decorator['function'](message)
            elif type(decorator['command']) == list:
                if message.command in decorator['command']:
                    decorator['function'](message)
        
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
        
