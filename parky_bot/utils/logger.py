import logging
import sys
import queue
from colorlog import ColoredFormatter


LOG_FORMAT = '%(levelname)-8s | {%(filename)s:%(funcName)s:%(lineno)d} | %(message)s'
LOG_FORMAT_CONSOLE = '%(levelname)-8s | %(message)s'
LOG_FORMAT_COLORED = '%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s'

CONSOLE_QUEUE = queue.Queue()


class ConsoleQueue(logging.Handler):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def emit(self, message):
        self.queue.put(message)


def configure_logger(logger: logging.Logger, level: int):
    """Configures a particular logging.Logger object with handlers.

    Args:
        logger (logging.Logger): logging object.
        handlers (list): list of logging handlers to add
        level (int): logging level, eg logging.DEBUG
    """

    if not logger.handlers:
        # Defining handlers
        file_handler = logging.FileHandler(filename='parky_logs.log')
        stdout_handler = logging.StreamHandler(sys.stdout) #sys.stdout is not necessary over stderr
        console_handler = ConsoleQueue(CONSOLE_QUEUE)
        #stderr_handler = logging.StreamHandler()

        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }

        # Defining formatters
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        stdout_handler.setFormatter(ColoredFormatter(LOG_FORMAT_COLORED, log_colors=log_colors))
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT_CONSOLE))
        #stderr_handler.setFormatter(ColoredFormatter(LOG_FORMAT_COLORED))

        # Adding handlers
        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)
        logger.addHandler(console_handler)
        #logger.addHandler(stderr_handler)

        # Defining levels
        file_handler.setLevel(logging.WARN) # Hardcoding this
        stdout_handler.setLevel(level)
        console_handler.setLevel(level)
        logger.setLevel(level) # Without this line, console log is ignored for some reason.

def get_logger():
    """This function returns a single logging object.

    Returns:
        Logger: logger object.
    """

    logger = logging.getLogger('parky_bot')

    return logger

def get_console_queue():
    return CONSOLE_QUEUE
