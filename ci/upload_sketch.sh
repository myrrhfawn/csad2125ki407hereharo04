#!/bin/bash

# Задайте змінні
SKETCH_NAME="../COMServer/COMServer.ino"  # Назва вашого .ino файлу
BOARD="arduino:avr:nano"       # Змінити на вашу плату, якщо потрібно
PORT="/dev/ttyV0"           # Змінити на ваш порт, якщо потрібно

# Перевірка наявності Arduino CLI
if ! command -v ../bin/arduino-cli &> /dev/null
then
    echo "Arduino CLI не знайдено. Будь ласка, встановіть Arduino CLI."
    exit 1
fi

# Ініціалізація (можна коментувати, якщо вже ініціалізовано)
# arduino-cli config init

# Оновлення індексу платформ
../bin/arduino-cli core update-index

# Інсталяція платформи (можна коментувати, якщо вже інстальовано)
../bin/arduino-cli core install $BOARD

# Компіліруємо скетч
echo "Компіліруємо $SKETCH_NAME..."
../bin/arduino-cli compile --fqbn $BOARD $SKETCH_NAME

# Завантаження на плату
echo "Завантаження на плату $BOARD через порт $PORT..."
../bin/arduino-cli upload -p $PORT --fqbn $BOARD $SKETCH_NAME

echo "Завершено."
