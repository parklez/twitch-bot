import tkinter
from parky_bot.gui.themes.default import Theme
from parky_bot.gui.settings_window import SettingsWindow


class ButtonBar(tkinter.Frame):
    def __init__(self, parent, settings, **kwargs):
        super().__init__(parent, **kwargs)

        self.vol = settings

        self.settings_button = tkinter.Button(self,
                                              text='Settings',
                                              padx=10,
                                              bg=Theme.BUTTON_BG,
                                              fg=Theme.BUTTON_FG,
                                              command=self.open_settings)
        self.settings_button.grid(row=0, column=0, padx=10, pady=10)

        #https://pt.stackoverflow.com/questions/343574/como-inicializar-essa-fun%C3%A7%C3%A3o-de-photoimage-do-tkinter
        self.vol_emote = Theme.VOL_ICON
        self.vol_img = tkinter.PhotoImage(data=self.vol_emote)
        self.vol_img_label = tkinter.Label(self, image=self.vol_img, bg=Theme.BAR_BG)
        self.vol_img_label.grid(row=0, column=1, padx=(10, 0), sticky='e')

        self.vol_meter = tkinter.Scale(self, orient=tkinter.HORIZONTAL,
                                       bg=Theme.SLIDER_BG,
                                       fg=Theme.SLIDER_FG,
                                       length=130,
                                       activebackground=Theme.SLIDER_ACTIVE_BG,
                                       troughcolor=Theme.SLIDER_SLIDE_BG,
                                       highlightbackground=Theme.SLIDER_HL_BG,
                                       command=lambda vol: self.vol.update({'volume': int(vol)}))
        self.vol_meter.set(self.vol.get('volume', 100))
        self.vol_meter.grid(row=0, column=2, padx=10, sticky='e')

        self.columnconfigure(1, weight=1)

    def open_settings(self):
        SettingsWindow(self.vol)
