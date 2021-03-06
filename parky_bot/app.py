from parky_bot.settings import BOT, APP, RESOURCE_PATH, APP_PATH
from parky_bot.utils.plugin_loader import load_plugins


# Plugins
import parky_bot.plugins.core_twitch
import parky_bot.plugins.core_pat_love
import parky_bot.plugins.core_gtts
import parky_bot.plugins.core_sounds
import parky_bot.plugins.core_misc
import parky_bot.plugins.core_plugin_management

# Third party plugins
load_plugins(RESOURCE_PATH, 'parky_bot')
load_plugins(APP_PATH)

if __name__ == "__main__":
    APP.start()
    BOT.pooling()
