#!/bin/bash

if [ -n "$GITHUB_ENV" ]; then
  echo "export PATH=$PATH:$PWD/bin/" >> $GITHUB_ENV
else
  echo "export PATH=$PATH:$PWD/bin/" > ~/.bashrc
  source ~/.bashrc
fi

curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
arduino-cli config init

