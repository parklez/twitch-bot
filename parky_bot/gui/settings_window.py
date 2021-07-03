import tkinter
from parky_bot.gui.themes.default import Theme


class SettingsWindow(tkinter.Toplevel):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.wm_title('Settings')
        self.grab_set()

        self.minsize(500, 400)
        self.resizable(1, 0)
        self.configure(background=Theme.BG)

        self.irc_frame = IRCLabel(self, self.settings, text='IRC Chat', padx=10, pady=10)
        self.irc_frame.pack(fill=tkinter.X, padx=10, pady=10)

        self.api_frame = APILabel(self, self.settings, text='Twitch API', padx=10, pady=10)
        self.api_frame.pack(fill=tkinter.X, padx=10, pady=(0, 10))

        self.other_frame = OtherLabel(self, self.settings, text='Other', padx=10, pady=10)
        self.other_frame.pack(fill=tkinter.X, padx=10)

        self.save_button = tkinter.Button(self,
                                          text='Save',
                                          padx=10,
                                          bg=Theme.BG,
                                          fg=Theme.FG,
                                          highlightbackground=Theme.BG,
                                          command=self.save_fields)
        self.save_button.pack(anchor='se', expand=True, pady=10, padx=10)

    def save_fields(self):
        self.settings.update(self.api_frame.get_fields())
        self.settings.update(self.irc_frame.get_fields())
        self.settings.update(self.other_frame.get_fields())

        self.destroy()


class APILabel(tkinter.LabelFrame):
    def __init__(self, parent, settings, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure({'background': Theme.BG,
                        'fg': Theme.FG})

        # Channel
        self.channel_label = tkinter.Label(self, text='Channel: ', bg=Theme.BG, fg=Theme.FG)
        self.channel_label.grid(row=0, column=0, sticky='e', pady=(0, 10))
        self.channel_text = tkinter.StringVar()
        self.channel_entry = tkinter.Entry(self, textvariable=self.channel_text, bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.channel_entry.grid(row=0, column=1, sticky='we', pady=(0, 10))

        # Client ID
        self.client_id_label = tkinter.Label(self, text='Client ID: ', bg=Theme.BG, fg=Theme.FG)
        self.client_id_label.grid(row=1, column=0, sticky='e', pady=(0, 10))
        self.client_text = tkinter.StringVar()
        self.client_id_entry = tkinter.Entry(self, textvariable=self.client_text, bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.client_id_entry.grid(row=1, column=1, sticky='we', pady=(0, 10))

        # Token
        self.token_label = tkinter.Label(self, text='Token: ', bg=Theme.BG, fg=Theme.FG)
        self.token_label.grid(row=2, column=0, sticky='e')
        self.token_text = tkinter.StringVar()
        self.token_entry = tkinter.Entry(self, textvariable=self.token_text, bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.token_entry.grid(row=2, column=1, sticky='we')

        self.columnconfigure(1, weight=1)

        self.set_fields(settings['api'])

    def get_fields(self) -> dict:
        return {
            'api': {
                'channel': self.channel_text.get().lower(),
                'client_id': self.client_text.get().lower(),
                'token': self.token_text.get().lower()
            }
        }

    def set_fields(self, settings):
        self.channel_text.set(settings['channel'])
        self.client_text.set(settings['client_id'])
        self.token_text.set(settings['token'])


class IRCLabel(tkinter.LabelFrame):
    def __init__(self, parent, settings, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure({'background': Theme.BG,
                        'fg': Theme.FG})

        # Username
        self.username_label = tkinter.Label(self, text='Username: ', bg=Theme.BG, fg=Theme.FG)
        self.username_label.grid(row=0, column=0, sticky='e', pady=(0, 10))
        self.username_text = tkinter.StringVar()
        self.username_entry = tkinter.Entry(self, textvariable=self.username_text, bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.username_entry.grid(row=0, column=1, sticky='we', pady=(0, 10))

        # Channel
        self.channel_label = tkinter.Label(self, text='Channel: ', bg=Theme.BG, fg=Theme.FG)
        self.channel_label.grid(row=1, column=0, sticky='e', pady=(0, 10))
        self.channel_text = tkinter.StringVar()
        self.channel_entry = tkinter.Entry(self, textvariable=self.channel_text, bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.channel_entry.grid(row=1, column=1, sticky='we', pady=(0, 10))

        # Token
        self.token_label = tkinter.Label(self, text='Token: ', bg=Theme.BG, fg=Theme.FG)
        self.token_label.grid(row=2, column=0, sticky='e')
        self.token_text = tkinter.StringVar()
        self.token_entry = tkinter.Entry(self, textvariable=self.token_text, bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.token_entry.grid(row=2, column=1, sticky='we')

        self.columnconfigure(1, weight=1)

        self.set_fields(settings['irc'])

    def get_fields(self) -> dict:
        return {
            'irc': {
                'username': self.username_text.get().lower(),
                'channel': self.channel_text.get().lower(),
                'token': self.token_text.get().lower()
            }
        }

    def set_fields(self, settings):
        self.username_text.set(settings['username'])
        self.channel_text.set(settings['channel'])
        self.token_text.set(settings['token'])


class OtherLabel(tkinter.LabelFrame):
    def __init__(self, parent, settings, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure({'background': Theme.BG,
                        'fg': Theme.FG})

        # Logging
        self.log_label = tkinter.Label(self, text='Logging level: ', bg=Theme.BG, fg=Theme.FG)
        self.log_label.grid(row=0, column=0, sticky='e')
        self.log_text = tkinter.StringVar()
        self.log_entry = tkinter.Entry(self, textvariable=self.log_text,bg=Theme.BAR_BG, fg=Theme.FG, insertbackground=Theme.FG)
        self.log_entry.grid(row=0, column=1, sticky='we')

        self.columnconfigure(1, weight=1)

        self.set_fields(settings['logging'])

    def get_fields(self) -> dict:
        return {
            'logging': {
                'level': self.log_text.get().lower(),
            }
        }

    def set_fields(self, settings):
        self.log_text.set(settings['level'])

