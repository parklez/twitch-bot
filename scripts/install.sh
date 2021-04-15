#!/bin/sh

# Clone project
git clone https://github.com/parklez/twitch-bot.git 
cd twitch-bot

# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install vext.gi

# Shortcuts (Linux)
python scripts/make_shortcuts.py
chmod +x ~/Desktop/parkybot.desktop
chmod +x ~/.local/share/applications/parkybot.desktop

echo "Installation complete!"
