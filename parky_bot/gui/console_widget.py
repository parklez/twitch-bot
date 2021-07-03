import queue
import tkinter
from tkinter.scrolledtext import ScrolledText
from parky_bot.utils.logger import get_console_queue, get_logger
from parky_bot.models.message import Message
from parky_bot.gui.themes.default import Theme


LOGGER = get_logger()
QUEUE = get_console_queue()


class Console(tkinter.Frame):

    def __init__(self, parent, settings, **kwargs):
        super().__init__(parent, **kwargs)

        self.settings = settings

        self.console = ScrolledText(self,
                                    bg=Theme.CONSOLE_BG,
                                    highlightbackground=Theme.BG,
                                    highlightcolor=Theme.BG,
                                    wrap=tkinter.CHAR,
                                    width=40,
                                    height=10,
                                    state='disabled',
                                    relief='flat')

        # Despite setting height above, this widget gets expanded fully,
        # if the canvas is smaller than the height, will look odd.
        self.console.pack(fill=tkinter.BOTH,
                          expand=True)

        self.font = ('Helvetica', 11, 'bold')

        # Text color
        self.console.tag_config('TEXT',
                                foreground=Theme.CONSOLE_TEXT,
                                font=('Helvetica', 11),
                                spacing1=5,
                                spacing3=5)

        # Logging colors
        self.console.tag_config('INFO', foreground=Theme.LOG_INFO)
        self.console.tag_config('DEBUG', foreground=Theme.LOG_DEBUG)
        self.console.tag_config('ERROR', foreground=Theme.LOG_ERROR)
        self.console.tag_config('WARNING', foreground=Theme.LOG_WARNING)
        self.console.tag_config('CRITICAL', foreground=Theme.LOG_CRITICAL)
        self.console.focus()

        if not self.settings['irc']['username']:
            self.welcome()
        else:
            self.after(100, self.pooling)

    def pooling(self):
        while 1:
            try:
                message = QUEUE.get(block=False)
                self.insert(message)
            except queue.Empty:
                break
        self.after(100, self.pooling)

    def insert(self, text):
        self.console.configure(state='normal') # Allow writing
        try: # Tcl can't render some characters
            if isinstance(text, Message):
                user_color = 'lightblue1' if not text.tags.get('color') else text.tags.get('color')
                self.console.tag_config(text.sender,
                                        font=self.font,
                                        foreground=user_color,
                                        spacing1=5,
                                        spacing3=5)
                self.console.insert(tkinter.END, text.sender, text.sender)
                self.console.insert(tkinter.END, f': {text.message}\n', 'TEXT')
            else:
                message = LOGGER.handlers[1].format(text) # This is not a good way to access this
                self.console.insert(tkinter.END, f'{message}\n', text.levelname)

        except tkinter.TclError as e:
            if isinstance(text, Message):
                # Replace every char outside of Tcl's allowed range with the ? char.
                text.message = ''.join((ch if ord(ch) <= 0xFFFF else '\uFFFD') for ch in text.message)
                self.console.insert(tkinter.END, f': {text.message}\n', 'TEXT')

            else:
                self.console.insert(tkinter.END, f'{e}\n', 'ERROR')

        self.console.configure(state='disabled') # Disallow writing
        self.console.yview(tkinter.END)

    def welcome(self):
        self.font = ('TkDefaultFont', 11, 'bold')
        self.console.tag_configure('lightblue', foreground='lightblue1', font=self.font, justify='center')
        self.console.tag_configure('white', foreground='white', font=self.font)
        self.console.tag_configure('orange', foreground='orange', font=self.font)
        self.console.tag_configure('pink', foreground='#FFC8D7', font=self.font)
        self.console.tag_configure('red', foreground='red', font=self.font, spacing1=2, spacing3=2)
        self.console.tag_config('grey', foreground='grey', font=('TkDefaultFont', 8, 'bold'))

        self.console.configure(state='normal')
        self.console.insert(tkinter.END, 'Welcome to parky\'s twitch bot!\n\n', 'lightblue')
        self.console.insert(tkinter.END, '\n', 'white')
        self.console.insert(tkinter.END, 'Quick setup:\n', 'orange')
        self.console.insert(tkinter.END, '\n', 'white')
        self.console.insert(tkinter.END, '1', 'red')
        self.console.insert(tkinter.END, '. Click on the "', 'white')

        self.settings_img = tkinter.PhotoImage(data=Theme.SETTINGS_ICON)
        self.console.image_create(tkinter.END, image=self.settings_img)

        self.console.insert(tkinter.END, '" button.\n', 'white')
        self.console.insert(tkinter.END, '2', 'red')
        self.console.insert(tkinter.END, '. Fill in IRC fields to gain chat access!\n', 'white')
        self.console.insert(tkinter.END, '3', 'red')
        self.console.insert(tkinter.END, '. ', 'white')
        self.console.insert(tkinter.END, 'Fill in Twitch API to gain access to channel metadata, such as current title, game, uptime, followers... ', 'white')
        self.console.insert(tkinter.END, '(optional)\n', 'grey')
        self.console.insert(tkinter.END, '\n', 'TEXT')
        self.console.insert(tkinter.END, 'Restart the application for changes to apply!', 'pink')

        self.console.configure(state='disabled')
