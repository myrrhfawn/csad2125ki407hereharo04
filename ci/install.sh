#!/bin/bash

export PATH=$PATH:$PWD/bin/
if [ -n "$GITHUB_ENV" ]; then
  echo "export PATH=$PATH" >> $GITHUB_ENV
else
  echo "export PATH=$PATH" > ~/.bashrc
  source ~/.bashrc
fi

curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
arduino-cli config init
arduino-cli core install arduino:avr


