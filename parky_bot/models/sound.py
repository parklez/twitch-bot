import threading
import vlc


class Sound:
    
    def __init__(self, path):
        self.path = path
    
    def play(self):
        threading.Thread(target=Sound._play, args=(vlc.MediaPlayer(self.path),)).start()
    
    @staticmethod
    def _play(audio):
        audio.play()
        while audio.get_state() != vlc.State.Ended:
            pass
        audio.release()
