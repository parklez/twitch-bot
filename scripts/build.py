import os
import platform
import shutil
import subprocess


IGNORE_LIST_WIN = ['app.exe', 'python39.dll']
IGNORE_LIST_LINUX = ['libpython3.9.so.1.0', 
                     '_struct.cpython-39-x86_64-linux-gnu.so', 
                     'zlib.cpython-39-x86_64-linux-gnu.so']

IGNORE_LIST = ['bin', 'certifi','base_library.zip']
IGNORE_LIST += (IGNORE_LIST_WIN if platform.system() == 'Windows' else IGNORE_LIST_LINUX)

CWD = os.getcwd()
ICON_PATH = os.path.join(CWD, 'scripts', 'dog_pet_animal_japanese_shiba_inu_japan_icon_127300.ico')
SCRIPT_PATH = os.path.join(CWD, 'parky_bot', 'app.py')
HOOK_PATH = os.path.join(CWD, 'scripts', 'add_lib.py')
BUILD_PATH = os.path.join(CWD, 'dist', 'app')

subprocess.run(['pyinstaller',
                '--onedir',
                '--noconsole',
                '--icon', ICON_PATH,
                '--hidden-import', 'gtts',
                '--hidden-import', 'requests',
                '--hidden-import', 'audioplayer',
                '--runtime-hook', HOOK_PATH,
                SCRIPT_PATH])

# Moving files to 'lib'
os.makedirs(os.path.join(BUILD_PATH, 'bin'))

for file in os.listdir(BUILD_PATH):
    if file not in IGNORE_LIST:
        shutil.move(os.path.join(BUILD_PATH, file), os.path.join(BUILD_PATH, 'bin', file))

# Copying core plugins
shutil.copytree(os.path.join(CWD, 'plugins'), os.path.join(BUILD_PATH, 'plugins'))

# Deleting temporary folders
shutil.rmtree(os.path.join(CWD, 'build'))
