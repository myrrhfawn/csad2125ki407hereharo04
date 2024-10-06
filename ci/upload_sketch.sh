#!/bin/bash

SKETCH_NAME="../COMServer/COMServer.ino"  # Binary file name
BOARD="arduino:avr:nano"       # Board name
PORT="/dev/ttyV0"           # Path to UART port

# Uploadin to board
echo "Uploading sketch to $BOARD due $PORT..."
../bin/arduino-cli upload -p $PORT --fqbn $BOARD $SKETCH_NAME

echo "Success."