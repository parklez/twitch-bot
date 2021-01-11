import os
import shutil
import subprocess


IGNORE_LIST = ['lib', 'certifi', '_ctypes.pyd', 'app.exe', 'python37.dll', 'base_library.zip']
PROJECT_PATH = os.getcwd()
ICON_PATH = os.path.join(PROJECT_PATH, 'art', 'dog_pet_animal_japanese_shiba_inu_japan_icon_127300.ico')
APP_PATH = os.path.join(PROJECT_PATH, 'dist', 'app')

# Pyinstaller build - "--noconsole" to hide terminal
subprocess.run(["pyinstaller", "-y", "-i", ICON_PATH, "--runtime-hook", "add_lib.py",  "parky_bot/app.py", "--noconsole"])

# Moving files to 'lib'
os.makedirs(os.path.join(APP_PATH, 'lib'))

for file in os.listdir(APP_PATH):
    if file not in IGNORE_LIST:
        shutil.move(os.path.join(APP_PATH, file), os.path.join(APP_PATH, 'lib', file))

# Deleting temporary folders
shutil.rmtree(os.path.join(PROJECT_PATH, 'build'))

# Archiving
shutil.make_archive(base_name=APP_PATH,
                        format='zip',
                        base_dir=APP_PATH)
