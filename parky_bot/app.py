from parky_bot.settings import BOT

# Plugins
import parky_bot.plugins.core_twitch
import parky_bot.plugins.core_pat_love
import parky_bot.plugins.core_gtts
import parky_bot.plugins.core_sounds
import parky_bot.plugins.core_misc

if __name__ == "__main__":
    BOT.pooling()
