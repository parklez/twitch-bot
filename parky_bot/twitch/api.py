from datetime import datetime, timezone
import requests
from parky_bot.utils.logger import get_logger


LOGGER = get_logger()


class TwitchAPI:
    api_host = 'https://api.twitch.tv/helix'

    def __init__(self, client_id: str, token=None):
        """Class for interacting with the Twitch API Helix.

        Args:
            client_id (str): Client ID from bot application https://glass.twitch.tv/console/apps
            token (str, optional): Authorization token.
        """

        self.client_id = client_id
        self.token = token

        self.headers = {'Client-ID': self.client_id,
                        'Content-Type': 'application/json'}

        if self.token:
            self.add_token_to_headers(self.token)

        self.channel = '' # Username/Login from the channel connected to
        self.broadcaster_id = '' # Unique identifier of the above channel
        self.status = '' # Also known as stream title
        self.game = '' # Stream game

    def add_token_to_headers(self, token: str):
        self.headers['Authorization'] = f'Bearer {token}'

    def connect(self) -> None:
        """Connects to Twitch API in few steps:
        1. Checks if token is valid.
        2. Fetches user information and save its "_id" to be used in API calls.
        3. Fetches current channel state and save its title/game.
        """

        if not self.validate_token():
            return

        users = self.get_users([self.channel])
        user = users[0] if users else ''

        self.broadcaster_id = user.get('id', '')

        channel_info = self.get_channel_by_id(self.broadcaster_id)
        self.status = channel_info.get('title', '')
        self.game = channel_info.get('game_name', '')

    def validate_token(self) -> bool:
        # https://dev.twitch.tv/docs/authentication

        r = requests.get('https://id.twitch.tv/oauth2/validate',
                         headers=self.headers)
        if r.status_code == 200:
            LOGGER.debug(r.json())
            self.channel = r.json()['login']
            return True
        LOGGER.warning(f'Twitch API validation [{r.status_code}]: {r.text}')
        return False

    def get_users(self, users: list) -> list:
        # https://dev.twitch.tv/docs/api/reference#get-users

        users = '&login='.join(users)
        r = requests.get(f'{self.api_host}' \
                         f'/users?login={users}',
                         headers=self.headers)
        if r.status_code == 200:
            return r.json()['data']
        LOGGER.warning(f'get_users [{r.status_code}]: {r.text}')
        return []

    def get_channel_by_id(self, broadcaster_id: str) -> dict:
        # https://dev.twitch.tv/docs/api/reference#get-channel-information

        r = requests.get(f'{self.api_host}/channels' \
                         f'?broadcaster_id={broadcaster_id}',
                         headers=self.headers)
        if r.status_code == 200:
            return r.json()['data'][0]
        LOGGER.warning(f'get_channel_by_id [{r.status_code}]: {r.text}')
        return {}

    def get_games(self, game_title: str) -> tuple[str, str]:
        # https://dev.twitch.tv/docs/api/reference#get-games

        r = requests.get(f'{self.api_host}' \
                         f'/games?name={game_title}',
                         headers=self.headers
        )

        if r.status_code == 200:
            try:
                result = r.json()['data'][0]
                return result['id'], result['name']
            except (KeyError, IndexError):
                LOGGER.info(f'get_games: Twitch didn\'t find "{game_title}"')
        return '', ''

    def update_stream(self, game_title=None, stream_title='') -> bool:
        # https://dev.twitch.tv/docs/api/reference#modify-channel-information

        if game_title == None and stream_title == '':
            return

        post_data = {}
        game_proper_title = None

        # In case of query
        if game_title:
            game_id, game_proper_title = self.get_games(game_title)
            if game_id:
                post_data['game_id'] = game_id

        # In case of unsetting the game
        elif game_title == '':
            game_id = ''

        if stream_title:
            post_data['title'] = stream_title

        # In case of bad game query
        if not post_data:
            return

        r = requests.patch(f'{self.api_host}' \
                            f'/channels?broadcaster_id={self.broadcaster_id}',
                            json=post_data,
                            headers=self.headers)

        if r.status_code == 204:
            self.game = game_proper_title if game_proper_title else self.game
            self.status = stream_title
            return True

        LOGGER.warning(f'update_stream [{r.status_code}]: {r.text}')
        return False

    def get_streams(self, user_ids: list) -> list:
        # https://dev.twitch.tv/docs/api/reference#get-streams

        user_ids = '&user_id='.join(user_ids)
        r = requests.get(f'{self.api_host}' \
                         f'/streams/&user_id={user_ids}',
                         headers=self.headers)
        if r.status_code == 200:
            return r.json()['data']
        LOGGER.warning(f'get_streams [{r.status_code}]: {r.text}')
        return []

    def _get_stream_startup_timestamp(self) -> str:
        stream_info = self.get_streams([self.broadcaster_id])
        if not stream_info:
            return ''

        return stream_info['data'][0]['started_at']

    def get_uptime(self) -> str:
        created_at = self._get_stream_startup_timestamp()

        if not created_at:
            return ''

        # json format: "2016-12-14T22:49:56Z" - UTC 0
        then = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
        # timezone.utc sets zone to 0 utc, replace turns this object naive.
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return now - then
