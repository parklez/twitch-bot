import socket

import requests


class TwitchIRC:
    def __init__(self, username, channel, token):
        """
        IRC client with Twitch specific methods.
        Get your access token here www.twitchapps.com/tmi/
        """
        self.username = username
        self.token = token
        self.channel = '#' + channel
        self.host = 'irc.twitch.tv'
        self.port = 6667
        self.irc_sock = socket.socket()
        self.welcome()

    def welcome(self):
        """
        This function connects to twitch IRC, sends token & nickname and joins a channel.
        """
        self.irc_sock.connect((self.host, self.port))
        self.send_token()
        self.send_nick()
        self.join_channel()

    def disconnect(self):
        self.irc_sock.close()
        
    def send(self, data):
        """
        This function converts data into bytes with UTF-8 encoding then socket.send()
        """
        self.irc_sock.send(bytes(data, 'UTF-8'))

    def send_pong(self):
        self.send("PONG :tmi.twitch.tv\r\n")

    def send_nick(self):
        self.send("NICK {}\r\n".format(self.username))

    def send_token(self):
        self.send("PASS {}\r\n".format(self.token))

    def join_channel(self):
        self.send("JOIN {}\r\n".format(self.channel))

    def part_channel(self):
        self.send("PART {}\r\n".format(self.channel))

    def send_message(self, message):
        self.send("PRIVMSG {} :{}\r\n".format(self.channel, message))
        

class TwitchAPI:
    def __init__(self, client_id, channel, token=None):
        """
        Basic Twitch API calls using kraken v5
        
        client_id = client id from your bot application <string> https://glass.twitch.tv/console/apps
        token = token for "user_read channel_editor" scopes <string> https://twitchapps.com/tokengen/
        channel = username of the channel authorized above <string>
        
        Methods:
        
            get_user: retrieves a json with user data
            retrieve_channel_id: returns id of the json above
            get_channel_by_id: returns a json with public channel info
            update_status: requests title update
            update_game: requests game update
            
        """
        self.client_id = client_id
        self.token = token
        self.channel = channel
        self.base_api = "https://api.twitch.tv/kraken/"
        self.last_call = ""
        
        self.headers = {'Client-ID': self.client_id,
                        'Accept': 'application/vnd.twitchtv.v5+json'}
                        
        if self.token:
            self.headers['Authorization'] = 'OAuth ' + self.token
            
            
        self.user = self.get_user()
        self.channel_id = self.retrieve_channel_id()
        self.channel_info = self.get_channel_by_id()
        self.recent_followers = self.retrieve_followers()
        
    def get_user(self):
        r = requests.get(self.base_api + 'user', headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            print('[Twitch API] get_user():', r.text)
        
    def retrieve_channel_id(self):
        if type(self.user) == dict:
            return self.user["_id"]
        else:
            print('[Twitch API] retrieve_channel_id(): No "_id" was found.')
            return None

    def get_channel_by_id(self):
        r = requests.get(self.base_api + "channels/" + self.channel_id, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            print('[Twitch API] get_channel_by_id():', r.text)
            return None
            
    def update_game(self, game_title):
        data = {'game': game_title}
        post_data = {'channel': data}
        response = requests.put(self.base_api + 'channels/' + self.channel_id, json=post_data, headers=self.headers)
        
        if response.status_code == 200:
            self.last_call = 'Game updated: ' + game_title
        else:
            self.last_call = response.text

    def update_status(self, stream_title):
        data = {'status': stream_title}
        post_data = {'channel': data}
        response = requests.put(self.base_api + 'channels/' + self.channel_id, json=post_data, headers=self.headers)

        if response.status_code == 200:
            self.last_call = 'Status updated: ' + stream_title
        else:
            self.last_call = response.text
            
    def retrieve_followers(self, count=5):
        count = str(count)
        followers = list()
        response = requests.get(self.base_api + 'channels/' + self.channel_id + '/follows?limit=' + count, headers=self.headers)
        if response.status_code == 200:
            for block in response.json()["follows"]:
                followers.append(block["user"]["display_name"])
        else:
            print('[Twitch API] retrieve_followers():', response.text)
            
        return followers
        
    def check_for_new_followers(self):
        latest_followers = self.retrieve_followers()
        new_followers = []
        
        for user in latest_followers:
            if user not in self.recent_followers:
                new_followers.append(user)
                
        self.recent_followers = latest_followers
        
        return new_followers
