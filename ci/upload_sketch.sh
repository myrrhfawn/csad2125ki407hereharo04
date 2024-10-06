#!/bin/bash

SKETCH_NAME="../COMServer/COMServer.ino"  # Binary file name
BOARD="arduino:avr:nano"       # Board name
PORT="/dev/ttyV0"           # Path to UART port
export PATH=$PATH:$PWD/bin/

# Uploadin to board
echo "Uploading sketch to $BOARD due $PORT..."
arduino-cli upload -p $PORT --fqbn $BOARD --input-dir ./build $SKETCH_NAME

echo "Success."