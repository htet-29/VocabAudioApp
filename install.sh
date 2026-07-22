#!/usr/bin/env bash

set -e

echo "Installing Vocab Audio Generator..."

#1. Create target directories if they don't exist
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons/hicolor/256x256/apps

#2. Copy binary
if [ -f "./dist/vocab-audio" ]; then
  cp ./dist/vocab-audio ~/.local/bin/
  chmod +x ~/.local/bin/vocab-audio
else
  echo "Error: Binary ./dist/vocab-audio not found. Run PyInstaller first."
  exit 1
fi

#3. Copy Icon
if [ -f "./assets/icon.png" ]; then
  cp ./assets/icon.png ~/.local/share/icons/hicolor/256x256/apps/vocab-audio-icon.png
fi

#4. Copy Desktop Entry
cp ./vocab-audio.desktop ~/.local/share/applications/

#5. Refresh Desktop Database
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database ~/.local/share/applications
fi

echo "Installation complete! Search for 'Vocab Audio Generator' in your applications menu."
