import queue
import tkinter
from tkinter.scrolledtext import ScrolledText
from parky_bot.utils.logger import get_console_queue, get_logger
from parky_bot.models.message import Message
from parky_bot.gui.themes.default import Theme


LOGGER = get_logger()
QUEUE = get_console_queue()


class Console(tkinter.Frame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.console = ScrolledText(self,
                                    bg=Theme.CONSOLE_BG,
                                    wrap=tkinter.CHAR,
                                    width=40,
                                    height=10,
                                    state='disabled')

        # Despite setting height above, this widget gets expanded fully,
        # if the canvas is smaller than the height, will look odd.
        self.console.pack(fill=tkinter.BOTH,
                          expand=True)

        # Text color
        self.console.tag_config('TEXT', foreground=Theme.HL, font='bold')

        # Logging colors
        self.console.tag_config('INFO', foreground=Theme.LOG_INFO)
        self.console.tag_config('DEBUG', foreground=Theme.LOG_DEBUG)
        self.console.tag_config('ERROR', foreground=Theme.LOG_ERROR)
        self.console.tag_config('WARNING', foreground=Theme.LOG_WARNING)
        self.console.tag_config('CRITICAL', foreground=Theme.LOG_CRITICAL)
        self.console.focus()
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
                self.console.tag_config(text.sender,
                                        font='bold',
                                        foreground=text.tags.get('color', 'lightblue1'))
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
