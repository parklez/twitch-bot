import socket
import time
import datetime
import threading

import requests


class TwitchIRC:
    def __init__(self, username, channel, token):
        """
        IRC client with Twitch specific methods.
        Get your access token at www.twitchapps.com/tmi/
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
        channel = username of the channel authorized above <string>
        token = token for "user_read channel_editor" scopes <string> https://twitchapps.com/tokengen/
        
        Methods:
            TODO: REWRITE
            
        """
        self.base_api = "https://api.twitch.tv/kraken/"
        self.client_id = client_id
        self.channel = channel
        self.token = token
        
        self.headers = {'Client-ID': self.client_id,
                        'Accept': 'application/vnd.twitchtv.v5+json'}
                        
        if self.token:
            self.headers['Authorization'] = 'OAuth ' + self.token
            
        self.user = None
        self.channel_id = ''
        self.title = ''
        self.game = ''
        self.last_call = ''
        
        self.channel_info = None
        self.recent_followers = []
        
        self.connect()
        
    def connect(self):
        user = threading.Thread(target=self.get_user)
        info = threading.Thread(target=self.get_channel_by_id)
        followers = threading.Thread(target=self.retrieve_followers)
        
        user.start()
        user.join()
        
        self.channel_id = self.fetch_channel_id()
        
        info.start()
        followers.start()
        
        info.join()
        self.status = self.fetch_status()
        self.game = self.fetch_game()

    def get_user(self):
        #https://dev.twitch.tv/docs/v5/#getting-a-client-id
        r = requests.get(self.base_api + 'user', headers=self.headers)
        
        if r.status_code == 200:
            self.user = r.json()
            return r.json()
        else:
            print('[Twitch API] get_user_json():', r.text)
        
    def fetch_channel_id(self):
        if type(self.user) == dict:
            return self.user["_id"]
        else:
            print('[Twitch API] fetch_channel_id(): No "_id" was found.')
            return None

    def get_channel_by_id(self):
        #https://dev.twitch.tv/docs/v5/reference/channels/#get-channel-by-id

        if self.channel_id:
            r = requests.get(self.base_api + "channels/" + self.channel_id, headers=self.headers)
        else:
            print('[Twitch API] get_channel_by_id: channel ID is None.')
            return

        if r.status_code == 200:
            self.channel_info = r.json()
            return r.json()
        else:
            print('[Twitch API] get_channel_by_id():', r.text)
            return None

    def fetch_status(self):
        if type(self.channel_info) == dict:
            return self.channel_info["status"]
            
        else:
            print('[Twitch API] fetch_status(): No "status" was found.')

    def fetch_game(self):
        if type(self.channel_info) == dict:
            return self.channel_info["game"]
            
        else:
            print('[Twitch API] fetch_game(): No "game" was found.')
    
    def update_game(self, game_title):
        data = {'game': game_title}
        post_data = {'channel': data}
        response = requests.put(self.base_api + 'channels/' + self.channel_id, json=post_data, headers=self.headers)
        
        if response.status_code == 200:
            self.game = game_title
            self.last_call = game_title
        else:
            self.last_call = response.text

    def update_status(self, stream_title):
        data = {'status': stream_title}
        post_data = {'channel': data}
        response = requests.put(self.base_api + 'channels/' + self.channel_id, json=post_data, headers=self.headers)

        if response.status_code == 200:
            self.status = stream_title
            self.last_call = stream_title
        else:
            self.last_call = response.text
            
    def retrieve_followers(self, count=5):
        count = str(count)
        followers = list()

        if self.channel_id:
            response = requests.get(self.base_api + 'channels/' + self.channel_id + '/follows?limit=' + count, headers=self.headers)
        else:
            print('[Twitch API] retrieve_followers: channel ID is None.')
            return
        
        if response.status_code == 200:
            for block in response.json()["follows"]:
                followers.append(block["user"]["display_name"])
        else:
            print('[Twitch API] _retrieve_followers():', response.text)
            
        self.recent_followers = followers
        return followers
        
    def check_for_new_followers(self):
        latest_followers = self.retrieve_followers()
        new_followers = []
        
        for user in latest_followers:
            if user not in self.recent_followers:
                new_followers.append(user)
                
        self.recent_followers = latest_followers
        
        return new_followers
        
    def get_stream_by_user(self):
        #https://dev.twitch.tv/docs/v5/reference/streams/#get-stream-by-user
        response = requests.get(self.base_api + 'streams/' + self.channel_id, headers=self.headers)

        return response.json()
        
    def _get_current_stream_startup_time(self):
        json = self.get_stream_by_user()
        if json['stream'] != None:
            return json['stream']['created_at']
        else:
            return None
            
    def _convert(self, seconds):
        #https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        return (hour, min, sec)
        
    def get_uptime(self) -> str:
        #json format "2016-12-14T22:49:56Z"
        string = self._get_current_stream_startup_time()
        
        if not string:
            return "{} is currently not live.".format(self.channel)
        else:
            #Eventually find a better solution for this mess
            #TODO: streams over 24 hours won't increase the hour counter
            now = datetime.datetime.now()
            year, month, day = string.split("T")[0].split("-")
            hours, minutes, seconds = string[:-1].split("T")[1].split(":")
            then = datetime.datetime(int(year), int(month), int(day), int(hours), int(minutes), int(seconds))
            delta = now - then
            uptime = self._convert(delta.seconds)
            
            return "{} has been live for {} hours, {} minutes, {} seconds.".format(self.channel, uptime[0], uptime[1], uptime[2])
          
    def get_users(self, username) -> str:
        #https://dev.twitch.tv/docs/v5/reference/users/#get-users
        
        r = requests.get(self.base_api + 'users?login=' + username, headers=self.headers)
        return r.json()
        
