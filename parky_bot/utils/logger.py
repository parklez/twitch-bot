import logging
import queue


LOG_FORMAT = '%(levelname)-8s | %(message)s'
CONSOLE_QUEUE = queue.Queue()


class ConsoleQueue(logging.Handler):
    def __init__(self, queue: queue.Queue):
        """Logging.Handler that sends logs to a Queue object.

        Args:
            queue (queue.Queue): Queue object to receive the log.
        """
        super().__init__()
        self.queue = queue

    def emit(self, message):
        self.queue.put(message)


def configure_logger(logger: logging.Logger, level: int):
    """Configures several loggers of the application, once.

    Args:
        logger (logging.Logger): logging object.
        level (int): logging level
    """

    if not logger.handlers:
        # Defining handlers
        stdout_handler = logging.StreamHandler()
        console_handler = ConsoleQueue(CONSOLE_QUEUE)

        # Defining formatters
        stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        # Adding handlers
        logger.addHandler(stdout_handler)
        logger.addHandler(console_handler)

        # Defining levels
        stdout_handler.setLevel(logging.DEBUG)  # Hardcoded
        console_handler.setLevel(level)
        logger.setLevel(logging.DEBUG)  # Minimal global logging level.
        logger.propagate = False  # Stops duplicated logging in virtual envs


def get_logger():
    """This function returns a single logging object.

    Returns:
        Logger: logger object.
    """

    logger = logging.getLogger('parky_bot')

    return logger


def get_console_queue():
    return CONSOLE_QUEUE
