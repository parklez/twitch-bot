import tkinter
from parky_bot.gui.themes.default import Theme
from parky_bot.gui.console_widget import Console
from parky_bot.gui.buttons_widget import ButtonBar
from parky_bot.gui.input_widget import InputBar


try: # This allows Windows 10 to scale the window for high DPI monitors.
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


class Application:

    def __init__(self, bot, settings):
        self.app = tkinter.Tk()
        self.settings = settings

        self.app.configure(background=Theme.BG)
        self.app.iconphoto(True, tkinter.PhotoImage(data=Theme.WM_ICON))
        self.app.title('parky\'s twitch-bot')
        self.app.minsize(300, 400)
        self.app.geometry("500x400")

        self.button_bar = ButtonBar(self.app, bot, self.settings, bg=Theme.BAR_BG)
        self.button_bar.pack(fill=tkinter.X)

        self.console = Console(self.app, self.settings)
        self.console.pack(fill=tkinter.BOTH,
                          pady=10,
                          padx=10,
                          expand=True)

        self.send = InputBar(self.app, bot, bg=Theme.BAR_BG)
        self.send.pack(fill=tkinter.X, side=tkinter.BOTTOM)

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bot = bot
        try:
            self.app.mainloop()
        except KeyboardInterrupt:
            self.on_closing()

    def on_closing(self):
        self.app.destroy()
        #import gc
        #https://pysimplegui.readthedocs.io/en/latest/#multiple-threads
        # self.button_bar = None
        # self.console = None
        # self.send = None
        # gc.collect()

        self.bot.disconnect()
