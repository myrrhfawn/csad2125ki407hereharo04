#!/bin/bash

BOARD="arduino:avr:nano"       # Board name
if [ -n "$GITHUB_WORKSPACE" ]; then
  SKETCH_NAME="$GITHUB_WORKSPACE/COMServer/COMServer.ino"  # Binary file name
else
  SKETCH_NAME="../COMServer/COMServer.ino"  # Binary file name
fi

export PATH=$PATH:$PWD/bin/

sudo apt-get install tree
tree ../
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
echo "Compile $SKETCH_NAME"
arduino-cli compile --fqbn $BOARD --output-dir ./build --verbose $SKETCH_NAME
