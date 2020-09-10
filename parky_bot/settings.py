import os
from parky_bot.utils.file_manager import load_json, make_dir, create_default_json


SOUNDS = load_json("parky_bot/data/sounds.json")
VOLUME = 80
SETTINGS = load_json("parky_bot/data/settings.json")
