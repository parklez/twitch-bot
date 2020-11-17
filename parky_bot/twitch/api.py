import datetime
import threading
import requests
from parky_bot.utils.logger import get_logger


class TwitchAPI:
    def __init__(self, client_id, channel, token=None):
        """Class for interacting with the Twitch API.

        Args:
            client_id (str): client id from your bot application https://glass.twitch.tv/console/apps
            channel (str): channel's username
            token (str, optional): Authorization token for "user_read channel_editor" scopes https://twitchapps.com/tokengen/. Defaults to None.
        """
        self.base_api = "https://api.twitch.tv/kraken/"
        self.client_id = client_id
        self.channel = channel
        self.token = token
        self._logger = get_logger()
        
        self.headers = {'Client-ID': self.client_id,
                        'Accept': 'application/vnd.twitchtv.v5+json'}
                        
        if self.token:
            self.headers['Authorization'] = f'OAuth {self.token}'
            
        self.user = {}
        self.channel_id = ''
        self.status = ''
        self.game = ''
        self.channel_info = {}
        
        self.connect()
        
    def connect(self):
        access, access_info = self.validate_token()
        if access != 200:
            self._logger.critical(f'Twitch API returned code "{access}": {access_info}')
            self._logger.critical('Generate a new token at https://twitchapps.com/tokengen/')
            return
            
        user = threading.Thread(target=self.get_user)
        info = threading.Thread(target=self.get_channel_by_id)
        
        user.start()
        user.join()
        
        self.channel_id = self.user.get('_id', '')
        
        info.start()
        
        info.join()
        self.status = self.fetch_status()
        self.game = self.fetch_game()

    def validate_token(self):
        #https://dev.twitch.tv/docs/authentication
        token = f'OAuth {self.token}'
        headers = {'Authorization': token}
        r = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers)
        return r.status_code, r.json()

    def get_user(self):
        #https://dev.twitch.tv/docs/v5/#getting-a-client-id
        r = requests.get(self.base_api + 'user', headers=self.headers)
        
        if r.status_code == 200:
            self.user = r.json()
        return r.json()

    def get_channel_by_id(self):
        #https://dev.twitch.tv/docs/v5/reference/channels/#get-channel-by-id
        r = requests.get(self.base_api + "channels/" + self.channel_id, headers=self.headers)
        
        if r.status_code == 200:
            self.channel_info = r.json()
        return r.json()

    def fetch_status(self):
        return self.channel_info.get('status')

    def fetch_game(self):
        return self.channel_info.get('game')
    
    def update_game(self, game_title):
        post_data = {
            'channel': {
                'game': game_title
            }
        }
        
        response = requests.put(self.base_api + 'channels/' + self.channel_id, json=post_data, headers=self.headers)
        
        if response.status_code == 200:
            self.game = game_title
        return response

    def update_status(self, stream_title):
        post_data = {
            'channel': {
                'status': stream_title
            }
        }

        response = requests.put(self.base_api + 'channels/' + self.channel_id, json=post_data, headers=self.headers)

        if response.status_code == 200:
            self.status = stream_title
        return response
    
    def retrieve_followers(self, count=5):
        followers = list()

        if self.channel_id:
            response = requests.get(self.base_api + 'channels/' + self.channel_id + '/follows?limit=' + str(count), headers=self.headers)
        else:
            print('[Twitch API] retrieve_followers: channel ID is None.')
            return followers
        
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
        
    def get_current_stream_startup_time(self):
        json = self.get_stream_by_user()
        if json.get('stream'):
            return json.get('stream').get('created_at')
        
    def get_uptime(self):
        #json format "2016-12-14T22:49:56Z"
        string = self.get_current_stream_startup_time()
        
        if string:
            then = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')
            now = datetime.datetime.now()
            diff = now - then
            
            return diff
          
    def get_users(self, username):
        #https://dev.twitch.tv/docs/v5/reference/users/#get-users
        r = requests.get(self.base_api + 'users?login=' + username, headers=self.headers)
        return r.json()
