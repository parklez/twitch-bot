import tkinter
from parky_bot.gui.themes.default import Theme
from parky_bot.gui.console_widget import Console

try: # This allows Windows 10 to scale the window for high DPI monitors.
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


class AppFrame(tkinter.Frame):
    #http://effbot.org/tkinterbook/tkinter-hello-again.htm
    #https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
    def __init__(self, app):
        super().__init__(app, bg=Theme.BG_COLOR)
        self.app = app
        """
        self.text = tkinter.Label(self.app,
                                  text='{parkybot}',
                                  font=('helvetica', 15),
                                  fg=Theme.FG_COLOR,
                                  bg=Theme.BG_COLOR)
        self.text.pack()
        """
        self.console = Console(self.app)


class Application:

    def __init__(self, bot):
        self.app = tkinter.Tk()

        self.app.configure(background=Theme.BG_COLOR)
        self.app.title('parkybot')
        self.app.minsize(600, 400)
        #self.app.resizable(0, 0)

        self.content = AppFrame(self.app)
        #self.content.pack()

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bot = bot
        self.app.mainloop()

    def on_closing(self):
        self.app.destroy()
        self.bot.irc.disconnect()
        self.bot.is_pooling = False
