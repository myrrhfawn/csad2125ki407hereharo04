#!/bin/bash

export PATH=$PATH:$PWD/bin/
BOARD="arduino:avr:nano"       # Board name
PORT="/dev/ttyV0"           # Path to UART port

if [ -n "$GITHUB_WORKSPACE" ]; then
  PROJECT_DIR = $$GITHUB_WORKSPACE
else
  PROJECT_DIR="/data/APKS/csad2125ki407hereharo04/"  # Binary file name
fi

SKETCH_NAME="$PROJECT_DIR/COMServer/COMServer.ino"  # Binary file name

# Uploadin to board
echo "Uploading sketch $SKETCH_NAME to $BOARD due $PORT..."
arduino-cli upload -p $PORT --fqbn $BOARD --input-dir $PROJECT_DIR/ci/build $SKETCH_NAME

echo "Success."