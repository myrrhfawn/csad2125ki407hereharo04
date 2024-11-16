#!/bin/bash
source .env

if [ -n "$GITHUB_WORKSPACE" ]; then
  PROJECT_DIR=$GITHUB_WORKSPACE
else
  PROJECT_DIR="$LOCAL_DIR/csad2125ki407hereharo04/"  # Binary file name
fi

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
$PROJECT_DIR/ci/bin/arduino-cli core update-index

# Compile sketch
echo "Compile $SKETCH_NAME"
$PROJECT_DIR/ci/bin/arduino-cli compile --fqbn $BOARD --output-dir "$PROJECT_DIR/ci/build" $SKETCH_NAME

tree $PROJECT_DIR
