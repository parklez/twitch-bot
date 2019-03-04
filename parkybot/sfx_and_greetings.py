import simpleaudio


class SFX:
    
    sounds = dict()
    
    def __init__(self, command, path, cooldown=False):
        self.command = command
        self.path = path
        self.sound = simpleaudio.WaveObject.from_wave_file(path)
        self.cooldown = cooldown
        self.lastplayed = 0
        SFX.sounds[command] = self
        
    def play_sound(self):
        if self.cooldown:
            return ## TODO
            
        else:
            self.sound.play()

            
class Greeter:

    people = dict()
    
    def __init__(self, username, message, sound=None):
        self.username = username
        self.message = message
        self.sound = sound
        self.greeted = False
        Greeter.people[username] = self
        
class Chain:
    
    chains = dict()
    
    def __init__(self, trigger, message, cooldown, counter=None, target=None):
        self.trigger = trigger
        self.message = message
        self.cooldown = cooldown
        self.target = target
        self.counter = counter
        
        Chain.chains[trigger] = self
        
    def count(self):
        self.counter += 1
        
