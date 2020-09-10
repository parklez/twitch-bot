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
                
                self._filter(m)
                
            data = ""
    
    def _filter(self, message: Message):
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
        
