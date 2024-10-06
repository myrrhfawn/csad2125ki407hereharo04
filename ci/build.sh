#!/bin/bash

if [ -n "$GITHUB_WORKSPACE" ]; then
  PROJECT_DIR=$GITHUB_WORKSPACE
else
  PROJECT_DIR="/data/APKS/csad2125ki407hereharo04/"  # Binary file name
fi

BOARD="arduino:avr:nano"       # Board name
SKETCH_NAME="$PROJECT_DIR/COMServer/COMServer.ino"  # Binary file name
export PATH=$PATH:$PWD/bin/

sudo apt-get install tree
tree $PROJECT_DIR

# Check Arduino CLI
if ! command -v arduino-cli &> /dev/null
then
    echo "Arduino CLI not found. Please install Arduino CLI."
    exit 1
fi

# Update plaform index
arduino-cli core update-index

# Compile sketch
echo "Compile $SKETCH_NAME"
arduino-cli compile --fqbn $BOARD --output-dir "$PROJECT_DIR/ci/build" $SKETCH_NAME
