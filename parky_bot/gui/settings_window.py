import tkinter
import threading
from parky_bot.gui.themes.default import Theme
from parky_bot.twitch.oauth_implicit_flow import handle_oauth, stop_auth


class SettingsWindow(tkinter.Toplevel):
    def __init__(self, bot, settings):
        super().__init__()

        self.settings = settings
        self.bot = bot

        self.wm_title('Settings')
        self.grab_set()

        self.minsize(350, 200)
        self.resizable(1, 0)
        self.configure(background=Theme.BG)

        self.irc_frame = IRCLabel(self, self.bot, self.settings, text='Chat', padx=10, pady=5)
        self.irc_frame.pack(fill=tkinter.X, padx=10, pady=5)

        self.api_frame = APILabel(self, self.bot, self.settings, text='Twitch API', padx=10, pady=5)
        self.api_frame.pack(fill=tkinter.X, padx=10, pady=(0, 5))

        self.other_frame = OtherLabel(self, self.settings, text='Misc', padx=10, pady=5)
        self.other_frame.pack(fill=tkinter.X, padx=10)

        self.save_button = tkinter.Button(self,
                                          text='Save',
                                          padx=10,
                                          bg=Theme.BG,
                                          fg=Theme.FG,
                                          highlightbackground=Theme.BG,
                                          command=self.save_fields)
        self.save_button.pack(anchor='se', expand=True, pady=10, padx=10)

        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def save_fields(self):
        self.settings['api']['client_id'] = self.api_frame.get_fields()
        self.settings['irc']['channel'] = self.irc_frame.get_fields()
        self.settings.update(self.other_frame.get_fields())

        self.restart_bot()
        stop_auth()
        self.destroy()

    def on_closing(self):
        stop_auth()
        self.destroy()

    def restart_bot(self):
        self.bot.disconnect()
        threading.Thread(target=self.bot.pooling).start()


class APILabel(tkinter.LabelFrame):
    def __init__(self, parent, bot, settings, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure({'background': Theme.BG,
                        'fg': Theme.FG})

        self.settings = settings
        self.bot = bot

        # Client ID
        self.client_id_label = tkinter.Label(self, text='Client ID: ', bg=Theme.BG, fg=Theme.FG)
        self.client_id_label.grid(row=1, column=0, sticky='e', pady=(0, 10))
        self.client_text = tkinter.StringVar()
        self.client_id_entry = tkinter.Entry(
            self, textvariable=self.client_text, bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.client_id_entry.grid(row=1, column=1, sticky='we', pady=(0, 10))

        # Auth
        self.button_open = tkinter.Button(self, text='Authorize API (Opens Browser)',
                                          bg=Theme.BG, fg=Theme.FG, command=self.start_oauth)
        self.button_open.grid(row=2, column=1, sticky='we', pady=(5, 5))

        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.set_fields(settings['api'])

    def get_fields(self) -> dict:
        return self.client_text.get().lower()

    def set_fields(self, settings):
        self.client_text.set(settings['client_id'])

    def start_oauth(self):
        self.auth_thread = threading.Thread(target=handle_oauth, args=(
            self.bot, self.settings, self.settings['api']['scopes'], 'api')).start()

class IRCLabel(tkinter.LabelFrame):
    def __init__(self, parent, bot, settings, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure({'background': Theme.BG,
                        'fg': Theme.FG})

        self.bot = bot
        self.settings = settings

        # Channel
        self.channel_label = tkinter.Label(self, text='Channel: ', bg=Theme.BG, fg=Theme.FG)
        self.channel_label.grid(row=1, column=0, sticky='e', pady=(0, 10))
        self.channel_text = tkinter.StringVar()
        self.channel_entry = tkinter.Entry(
            self, textvariable=self.channel_text, bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.channel_entry.grid(row=1, column=1, sticky='we', pady=(0, 10))

        # Auth
        self.button_open = tkinter.Button(
            self, text='Authorize Chat (Opens Browser)', bg=Theme.BG, fg=Theme.FG, command=self.start_oauth)
        self.button_open.grid(row=3, column=1, sticky='we', pady=(5, 5))

        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        self.set_fields(settings['irc'])

    def get_fields(self) -> dict:
        return self.channel_text.get().lower()

    def set_fields(self, settings):
        self.channel_text.set(settings['channel'])

    def start_oauth(self):
        self.auth_thread = threading.Thread(target=handle_oauth, args=(
            self.bot, self.settings, self.settings['irc']['scopes'], 'irc')).start()

class OtherLabel(tkinter.LabelFrame):

    log_labels = {
        10: 'debug',
        20: 'info',
        30: 'warning',
        40: 'error',
        50: 'critical'
    }

    log_levels = dict(map(reversed, log_labels.items()))

    def __init__(self, parent, settings, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure({'background': Theme.BG,
                        'fg': Theme.FG})

        self.log_label = tkinter.Label(self, text='Logging level: ', bg=Theme.BG, fg=Theme.FG)
        self.log_label.grid(row=0, column=0, sticky='e')

        self.log_option = tkinter.StringVar()
        self.log_entry = tkinter.OptionMenu(self, self.log_option, *self.log_labels.values())
        self.log_entry.grid(row=0, column=1, sticky='we')

        # Font size
        self.size_label = tkinter.Label(self, text='Font size: ', bg=Theme.BG, fg=Theme.FG)
        self.size_label.grid(row=1, column=0, sticky='e')
        self.size_text = tkinter.StringVar()
        self.size_entry = tkinter.Entry(self, textvariable=self.size_text, bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.size_entry.grid(row=1, column=1, sticky='we')

        self.columnconfigure(1, weight=1)

        self.set_fields(settings)

    def get_fields(self) -> dict:
        return {
            'logging': {
                'level': self.log_levels[self.log_option.get()]
            },
            'settings': {
                'font-size': int(self.size_text.get()),
            }
        }

    def set_fields(self, settings):
        curent_logging = settings.get('logging', {}).get('level', '20')
        self.log_option.set(self.log_labels[curent_logging])
        self.size_text.set(settings['settings']['font-size'])
