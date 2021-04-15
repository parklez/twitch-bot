#!/bin/sh

# Start from /scripts dir
BASEDIR=$(dirname $0)

# Erase everything
rm -r -f ${BASEDIR}/../../twitch-bot

# Remove shortcuts (Linux)
rm ~/Desktop/parkybot.desktop
rm ~/.local/share/applications/parkybot.desktop

echo "Uninstall complete!"
