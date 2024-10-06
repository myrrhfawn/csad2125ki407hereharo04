#!/bin/bash

export PATH=$PATH:$PWD/bin/
BOARD="arduino:avr:nano"       # Board name
PORT="/dev/ttyV0"           # Path to UART port

if [ -n "$GITHUB_WORKSPACE" ]; then
  SKETCH_NAME="$GITHUB_WORKSPACE/COMServer/COMServer.ino"  # Binary file name
else
  SKETCH_NAME="../COMServer/COMServer.ino"  # Binary file name
fi

# Uploadin to board
echo "Uploading sketch to $BOARD due $PORT..."
arduino-cli upload -p $PORT --fqbn $BOARD --input-dir ./build $SKETCH_NAME

echo "Success."