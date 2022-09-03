import tkinter
from parky_bot.gui.themes.default import Theme
from parky_bot.models.message import Message


class InputBar(tkinter.Frame):
    def __init__(self, parent, bot=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.bot = bot

        self.text = tkinter.StringVar()
        self.input_field = tkinter.Entry(self, textvariable=self.text,
                                         highlightbackground=Theme.BG)
        self.input_field.grid(column=0, row=0, padx=10,
                              pady=15, sticky=tkinter.EW)
        self.input_field.bind('<Return>', lambda _: self.send_msg())

        self.send_button = tkinter.Button(self, text='Send',
                                          command=self.send_msg,
                                          padx=10,
                                          bg=Theme.BUTTON_BG,
                                          fg=Theme.BUTTON_FG,
                                          highlightbackground=Theme.BAR_BG)
        self.send_button.grid(column=1, row=0, padx=(0, 10), sticky=tkinter.W)

        self.columnconfigure(0, weight=1)

    def send_msg(self):
        m = Message('')
        m.message = self.text.get().strip()
        m.sender = self.bot.irc.username
        m.badges = {'broadcaster': 1}  # Assumes owner is running it
        m.command = m.message.split()[0] if m.message else m.message
        if self.bot and self.bot.irc.username and m.message:
            self.bot.send_message(m.message)
            self.bot.filter(m)
        self.text.set('')
