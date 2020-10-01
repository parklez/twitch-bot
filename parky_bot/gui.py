import tkinter
from PIL import Image, ImageTk


FG_COLOR = '#D6F0DA'
BG_COLOR = '#303030'
PATH_TO_LOGO = 'parky_bot/resources/barkychan128.gif'


class ImageLabel(tkinter.Label):
    #https://stackoverflow.com/a/43770948
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        i = 0
        try:
            while 1:
                frame = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self.frames.append(frame)
                im.seek(i)
                i += 1
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


class AppFrame(tkinter.Frame):
    #http://effbot.org/tkinterbook/tkinter-hello-again.htm
    #https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
    def __init__(self, app):
        super().__init__(app, bg=BG_COLOR)
        self.app = app
        self.logo = ImageLabel(self.app, bg=BG_COLOR)
        self.logo.pack(pady=20)
        self.logo.load(PATH_TO_LOGO)

        self.text = tkinter.Label(self.app, text='{parkybot}', font=('helvetica', 15), fg=FG_COLOR, bg=BG_COLOR)
        self.text.pack()


class Application:

    def __init__(self, bot):
        self.app = tkinter.Tk()

        self.app.configure(background=BG_COLOR)
        self.app.title('parkybot')
        self.app.minsize(250, 200)
        self.app.resizable(0, 0)

        self.content = AppFrame(self.app)
        self.content.pack()

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bot = bot
        self.app.mainloop()

    def on_closing(self):
        self.app.destroy()
        self.bot.irc.disconnect()
        self.bot.is_pooling = False
