from parky_bot.settings import RESOURCE_PATH, APP_PATH, BOT
from parky_bot.utils.plugin_loader import load_plugins

# Plugins
import parky_bot.plugins.core_twitch
import parky_bot.plugins.core_pat_love
import parky_bot.plugins.core_gtts
import parky_bot.plugins.core_sounds
import parky_bot.plugins.core_misc

load_plugins(RESOURCE_PATH, 'parky_bot')
load_plugins(APP_PATH)

if __name__ == "__main__":
    BOT.pooling()
