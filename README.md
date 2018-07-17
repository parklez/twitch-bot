# twitch bot

### What can it do?
- Connect to Twitch chat via IRC, parse messages/sender
- Connect to Twitch API via kraken v5, allowing editors to change stream status/game
- Play .wav sounds asynchronously thanks to simpleaudio module
- Greet certain viewers once when they say something
- Print uptime in chat

### Dependencies
1. Python 3.6 or higher
2. Requests ```pip install requests```
3. Simple Audio ```pip install simpleaudio```

### Known issues
- simpleaudio doesn't support adjusting volume [see issue](https://github.com/hamiltron/py-simple-audio/issues/21)

### Disclaimer
This is still work in progress, along with the fact I'm also learning a lot.
