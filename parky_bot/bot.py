import time
from parky_bot.models.message import Message


class ParkyBot:
    def __init__(self, twitch=None, irc=None):
        self.twitch = twitch
        self.irc = irc
        self.handlers = []
        self.chatters = []
        self.is_pooling = True

    def pooling(self):
        if not self.irc:
            print("IRC client not set, not pooling!")
            return
        
        data = ""
        self.irc.irc_sock.setblocking(0)
        print("Now pooling...")
        
        while self.is_pooling:
            try:
                data = self.irc.irc_sock.recv(4096).decode('UTF-8')
            except (ConnectionAbortedError, OSError):
                time.sleep(0.1)
                continue

            if data == "":
                print("IRC client received 0 bytes, stopping...")
                self.is_pooling = False
                break

            if data == "PING :tmi.twitch.tv\r\n":
                self.irc.send_pong()
            
            else:
                # BUG: If the sender decides to send '\n' midstring, their message will be split.
                for line in data.splitlines():
                    m = Message(line)
                    
                    if m.sender not in self.chatters and m.sender:
                        self.chatters.append(m.sender)
                    
                    self._filter(m)
                
            data = ""
        print('Stopped pooling.')
    
    def _filter(self, message: Message):
        'Tests each filter on the Message object'
        for decorator in self.handlers:
            if isinstance(decorator['command'], str):
                if message.command == decorator['command']:
                    decorator['function'](message)
            elif isinstance(decorator['command'], list):
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
