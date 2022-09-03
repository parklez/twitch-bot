import tkinter
from parky_bot.gui.themes.default import Theme
from parky_bot.gui.settings_window import SettingsWindow


class ButtonBar(tkinter.Frame):
    def __init__(self, parent, bot, settings, **kwargs):
        super().__init__(parent, **kwargs)

        self.vol = settings
        self.bot = bot

        self.settings_img = tkinter.PhotoImage(data=Theme.SETTINGS_ICON)
        self.settings_button = tkinter.Button(self,
                                              image=self.settings_img,
                                              compound=tkinter.CENTER,
                                              # text='Settings',
                                              # padx=10,
                                              # pady=0,
                                              # height=28,
                                              bg=Theme.BUTTON_BG,
                                              fg=Theme.BUTTON_FG,
                                              highlightbackground=Theme.BAR_BG,
                                              # relief='flat',
                                              activebackground=Theme.BUTTON_BG,
                                              command=self.open_settings)
        self.settings_button.grid(row=0, column=0, padx=10)

        # https://stackoverflow.com/questions/42174987/how-do-i-use-the-base64-encoded-image-string-in-tkinter-label/42175482
        self.vol_img = tkinter.PhotoImage(data=Theme.VOL_ICON)
        self.vol_img_label = tkinter.Label(
            self, image=self.vol_img, bg=Theme.BAR_BG)
        self.vol_img_label.grid(row=0, column=1, padx=(10, 0), sticky='e')

        self.vol_meter = tkinter.Scale(self, orient=tkinter.HORIZONTAL,
                                       bg=Theme.SLIDER_BG,
                                       fg=Theme.SLIDER_FG,
                                       length=130,
                                       activebackground=Theme.SLIDER_ACTIVE_BG,
                                       troughcolor=Theme.SLIDER_SLIDE_BG,
                                       highlightbackground=Theme.SLIDER_HL_BG,
                                       command=lambda vol: self.set_vol(vol))
        self.vol_meter.set(self.get_vol())
        self.vol_meter.grid(row=0, column=2, padx=10, pady=5, sticky='e')

        self.columnconfigure(1, weight=1)

    def open_settings(self):
        SettingsWindow(self.bot, self.vol)

    def set_vol(self, vol: int) -> None:
        self.vol['settings']['volume'] = int(vol)

    def get_vol(self) -> int:
        return self.vol['settings'].get('volume', 100)
