#!/bin/bash
source .env

export PATH=$PATH:$PWD/bin/

if [ -n "$GITHUB_WORKSPACE" ]; then
  PROJECT_DIR = $GITHUB_WORKSPACE
else
  PROJECT_DIR="$LOCAL_DIR/csad2125ki407hereharo04"  # Binary file name
fi

SKETCH_NAME="$PROJECT_DIR/COMServer/COMServer.ino"  # Binary file name

# Uploadin to board
echo "Uploading sketch $SKETCH_NAME to $BOARD due $SERIAL_PORT..."
arduino-cli upload -p $SERIAL_PORT --fqbn $BOARD --input-dir $PROJECT_DIR/ci/build $SKETCH_NAME

echo "Success."