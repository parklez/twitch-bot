import logging
import sys
from colorlog import ColoredFormatter


LOG_FORMAT = '%(levelname)-8s | {%(filename)s:%(funcName)s:%(lineno)d} | %(message)s'
LOG_FORMAT_COLORED = '%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s'


def get_logger(level=logging.DEBUG):
    """This function returns a single logging object.

    Args:
        level (int, optional): Logging level. Defaults to logging.DEBUG.

    Returns:
        Logger: logger object.
    """

    logger = logging.getLogger('parky_bot')

    if not logger.handlers:
        file_handler = logging.FileHandler(filename='parky_logs.log')
        stdout_handler = logging.StreamHandler(sys.stdout) #sys.stdout is not necessary over stderr
        #stderr_handler = logging.StreamHandler()

        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }

        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        stdout_handler.setFormatter(ColoredFormatter(LOG_FORMAT_COLORED, log_colors=log_colors))
        #stderr_handler.setFormatter(ColoredFormatter(LOG_FORMAT_COLORED))

        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)
        #logger.addHandler(stderr_handler)

        file_handler.setLevel(logging.WARN)
        stdout_handler.setLevel(level)
        logger.setLevel(level) # Without this line, console log is ignored for some reason.

    return logger
