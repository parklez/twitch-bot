from parky_bot.settings import VOLUME
from vlc import MediaPlayer


class SFX:
    def __init__(self, path, cooldown=False):
        self.path = path
        self.cooldown = cooldown
        self.lastplayed = 0
        
    def play_sound(self, message):
        self.audio = MediaPlayer(self.path)
        self.audio.audio_set_volume(VOLUME)
        self.audio.play()

class Greeter:
    people = dict()
    
    def __init__(self, username, message, sound=None):
        self.username = username
        self.message = message
        self.sound = sound
        self.greeted = False
        Greeter.people[username] = self
