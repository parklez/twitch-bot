import os
import shutil
import subprocess


IGNORE_LIST = ['lib', 'certifi', 'app.exe', 'python39.dll', 'base_library.zip']
CWD = os.getcwd()
ICON_PATH = os.path.join(CWD, 'art', 'dog_pet_animal_japanese_shiba_inu_japan_icon_127300.ico')
SCRIPT_PATH = os.path.join(CWD, 'parky_bot', 'app.py')
BUILD_PATH = os.path.join(CWD, 'dist', 'app')

subprocess.run(['pyinstaller',
                '--onedir',
                '--noconsole',
                '--icon', ICON_PATH,
                '--hidden-import', 'gtts',
                '--hidden-import', 'requests',
                '--hidden-import', 'audioplayer',
                '--runtime-hook', 'add_lib.py',
                SCRIPT_PATH])

# Moving files to 'lib'
os.makedirs(os.path.join(BUILD_PATH, 'lib'))

for file in os.listdir(BUILD_PATH):
    if file not in IGNORE_LIST:
        shutil.move(os.path.join(BUILD_PATH, file), os.path.join(BUILD_PATH, 'lib', file))

# Copying core plugins
shutil.copytree(os.path.join(CWD, 'plugins'), os.path.join(BUILD_PATH, 'plugins'))

# Deleting temporary folders
shutil.rmtree(os.path.join(CWD, 'build'))

# Archiving
OUTPUT = os.path.join(CWD, 'parkybot')
shutil.make_archive(base_name=OUTPUT, # Output dir + name
                    format='zip',
                    base_dir='./',  # Base structure
                    root_dir=BUILD_PATH # Where to archive from
                    )
