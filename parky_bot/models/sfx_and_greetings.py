from parky_bot.settings import VOLUME
from vlc import MediaPlayer


class SFX:
    def __init__(self, path, cooldown=False):
        self.path = path
        self.cooldown = cooldown
        self.lastplayed = 0
        
    def play_sound(self, message):
        # FUTURE:
        # With the Message object, limit or cooldown specific users.
        print('play_sound.VOLUME', VOLUME)
        audio = MediaPlayer(self.path)
        audio.audio_set_volume(VOLUME)
        audio.play()


class Greeter:
    people = dict()
    
    def __init__(self, username, message, sound=None):
        self.username = username
        self.message = message
        self.sound = sound
        self.greeted = False
        Greeter.people[username] = self
