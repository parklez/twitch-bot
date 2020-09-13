from parky_bot.utils.file_manager import load_json, make_dir, create_default_json


# TODO: Pyinstaller code
"""
import os, sys
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

SETTINGS = load_json(os.path.join(application_path, 'settings.json'))
"""

VOLUME = 80
SETTINGS = load_json('parky_bot/settings.json')
