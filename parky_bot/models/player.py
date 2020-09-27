import threading
import vlc
import pafy


class Player:

    def __init__(self):
        self.instance = vlc.MediaPlayer()
        self.queue = []
        self.current = None
    
    def add_queue(self, link):
        link = pafy.new(link)
        link = link.audiostreams[0].url
        self.queue.append(link)
    
    def play(self):
        pass # Work in progress

    @staticmethod
    def _play(audio: vlc.MediaPlayer):
        audio.play()
        while audio.get_state() != vlc.State.Ended:
            pass
        audio.release()