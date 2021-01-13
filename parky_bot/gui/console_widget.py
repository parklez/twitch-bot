import queue
import tkinter
from tkinter.scrolledtext import ScrolledText
from parky_bot.utils.logger import get_console_queue, get_logger
from parky_bot.gui.themes.default import Theme


LOGGER = get_logger()
QUEUE = get_console_queue()


class Console:
    def __init__(self, app):
        self.app = app
        self.console = ScrolledText(self.app,
                                    bg=Theme.BG_COLOR,
                                    wrap=tkinter.WORD,
                                    width=40,
                                    height=10,
                                    state='disabled')

        self.console.pack(pady=10,
                          padx=10,
                          fill=tkinter.BOTH,
                          expand=True)

        # Logging colors
        self.console.tag_config('INFO', foreground=Theme.LOG_INFO)
        self.console.tag_config('DEBUG', foreground=Theme.LOG_DEBUG)
        self.console.tag_config('ERROR', foreground=Theme.LOG_ERROR)
        self.console.tag_config('WARNING', foreground=Theme.LOG_WARNING)
        self.console.tag_config('CRITICAL', foreground=Theme.LOG_CRITICAL, background='white')
        self.console.focus()
        self.app.after(100, self.pooling)

    def pooling(self):
        while 1:
            try:
                message = QUEUE.get(block=False)
                self.insert(message)
            except queue.Empty:
                break
        self.app.after(100, self.pooling)

    def insert(self, text):
        message = LOGGER.handlers[2].format(text) # This is not a good way to access this
        self.console.configure(state='normal')
        try: # Tcl can't render some characters
            self.console.insert(tkinter.END, f'{message}\n', text.levelname)
        except tkinter.TclError as e:
            self.console.insert(tkinter.END, f'{e}\n', 'ERROR')
        self.console.configure(state='disabled')
        self.console.yview(tkinter.END)
