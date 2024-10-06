#!/bin/bash

SKETCH_NAME="../COMServer/COMServer.ino"  # Binary file name
BOARD="arduino:avr:nano"       # Board name
PORT="/dev/ttyV0"           # Path to UART port

# Check Arduino CLI
if ! command -v arduino-cli &> /dev/null
then
    echo "Arduino CLI not found. Please install Arduino CLI."
    exit 1
fi

# Update plaform index
arduino-cli core update-index

# Intall Arduino board 
arduino-cli core install $BOARD

# Compile sketch
echo "Compile $SKETCH_NAME..."
arduino-cli compile --fqbn $BOARD $SKETCH_NAME
