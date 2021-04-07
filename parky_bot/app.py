from parky_bot.settings import start, APP_PATH
from parky_bot.utils.plugin_loader import load_plugins


# Load plugins
load_plugins(APP_PATH)

if __name__ == "__main__":
    start()
