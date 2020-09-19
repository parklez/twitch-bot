import threading
import vlc


class SFX:
    def __init__(self, path, cooldown=False):
        self.path = path
        
    def play_sound(self, message):
        threading.Thread(target=SFX._play, args=(vlc.MediaPlayer(self.path),)).start()

    @staticmethod
    def _play(audio):
        audio.play()
        while audio.get_state() != vlc.State.Ended:
            pass
        audio.release()

class Greeter:
    people = dict()
    
    def __init__(self, username, message, sound=None):
        self.username = username
        self.message = message
        self.sound = sound
        self.greeted = False
        Greeter.people[username] = self
