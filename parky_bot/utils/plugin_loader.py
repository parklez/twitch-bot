import os
import importlib
from parky_bot.utils.logger import get_logger


logger = get_logger()


def load_plugins(main_module_path: str, main_module_name='', plugins_folder='plugins'):
    plugins_dir = os.path.join(main_module_path, plugins_folder)
    if not os.path.isdir(plugins_dir):
        #logger.warn(f'Plugin folder not found: "{plugins_dir}"')
        return

    if main_module_name:
        main_module_name += '.'

    for file in os.listdir(plugins_dir):
        if file.endswith(".py"):
            try:
                importlib.import_module(f'{main_module_name}plugins.{file[:-3]}')
            except Exception as e:
                logger.error(e, exc_info=True)
