'''
This piece of code is responsible for starting 2 simple http servers:

- @ 1337 to serve an HTML which will parse the hashtag part of the browser address bar
- @ 1338 which will receive a request from that html page being served.

Once both completed their task, the api, irc and settings objects are updated!

# Twitch documentation
- Chat https://dev.twitch.tv/docs/irc/authenticate-bot
- API https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#implicit-grant-flow
'''
import webbrowser
import json
import hashlib
import os
import threading
import requests

from http.server import HTTPServer, SimpleHTTPRequestHandler
from parky_bot.utils.logger import get_logger


LOGGER = get_logger()
RESPONSE = None


class TokenRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        global RESPONSE

        try:
            length = int(self.headers.get('Content-Length'))
            payload_string = self.rfile.read(length).decode('utf-8')
            RESPONSE = json.loads(payload_string) if payload_string else None
        except Exception as error:
            LOGGER.error(error)


class RedirectRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)


def _send_stop_requests() -> None:
    try:
        requests.get('http://localhost:1337', timeout=1)
    except:
        pass
    try:
        requests.post('http://localhost:1338', timeout=1)
    except:
        pass


def stop_auth() -> None:
    if handle_oauth.handling:
        threading.Thread(target=_send_stop_requests).start()


def build_url(client_id: str, scopes: str) -> str:
    # TODO: randomly generated state
    state = hashlib.md5(
        'AlwaysRemberHappyDay'.encode()
    ).hexdigest()

    twitch_oauth = 'https://id.twitch.tv/oauth2/authorize'
    twitch_oauth += '?response_type=token' \
        f'&client_id={client_id}' \
        '&redirect_uri=http://localhost:1337' \
        f'&scope={scopes}' \
        f'&state={state}'
    return twitch_oauth


def handle_oauth(bot, settings: dict, scopes: str, auth_type: str) -> None:
    if handle_oauth.handling:
        LOGGER.info('Waiting for auth callback, please check your browser!')
        return

    handle_oauth.handling = True
    webbrowser.open(build_url(settings['api']['client_id'], scopes))

    html_server = HTTPServer(('', 1337), RedirectRequestHandler)
    token_server = HTTPServer(('', 1338), TokenRequestHandler)

    try:
        LOGGER.debug('Waiting for OAuth response...')

        a = threading.Thread(target=html_server.handle_request)
        b = threading.Thread(target=token_server.handle_request)

        a.start()
        b.start()

        # BUG: In not-so-rare cases browsers may not send post requests perfectly and cause this to hang
        a.join()
        b.join()

        if not RESPONSE:
            raise Exception('No response from Twitch, please try again!')

        LOGGER.debug(RESPONSE)

        token = RESPONSE['access_token']

        if auth_type == 'api':
            settings['api']['token'] = token
            bot.twitch.token = token
            bot.twitch.add_token_to_headers(token)
            if bot.twitch.validate_token():
                LOGGER.info('Twitch API authenticated!')
        else:
            settings['irc']['token'] = token
            bot.irc.token = token
            bot.irc.add_token_to_headers(token)
            username = bot.irc.validate_token()
            if username:
                LOGGER.info('Twitch Chat authenticated!')

    except Exception as error:
        LOGGER.debug('Error while handling OAuth request')
        LOGGER.error(error)

    finally:
        html_server.server_close()
        token_server.server_close()

        handle_oauth.handling = False


handle_oauth.handling = False
