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
        
    def play_sound(self, message):
        # FUTURE:
        # With the Message object, limit or cooldown specific users.
        self.sound.play()

            
class Greeter:

    people = dict()
    
    def __init__(self, username, message, sound=None):
        self.username = username
        self.message = message
        self.sound = sound
        self.greeted = False
        Greeter.people[username] = self

