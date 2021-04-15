import os
import platform


if platform.system() != 'Linux':
    raise NotImplementedError('This script only works on linux at the moment!')

ROOT = os.getcwd()
HOME = os.getenv('HOME')
DESKTOP = os.path.join(HOME, 'Desktop')
MENU = os.path.join(HOME, '.local', 'share', 'applications')
TEMPLATE = f"""[Desktop Entry]
Name=parkybot
Type=Application
Comment=Twitch IRC/API Bot
Terminal=false
Icon={ROOT}/scripts/dog_pet_animal_japanese_shiba_inu_japan_icon_127300.ico
Exec=sh scripts/start.sh
Path={ROOT}
StartupNotify=false
"""

for place in (DESKTOP, MENU):
    if os.path.isdir(place):
        with open(os.path.join(place, 'parkybot.desktop'), 'w') as _f:
            _f.write(TEMPLATE)
        print(f'Created shortcut at {place}')
