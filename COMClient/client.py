import serial
import time

# Налаштування серійного порту (замініть 'COM3' на '/tmp/ttyV1')
ser = serial.Serial('/tmp/ttyV1', 9600)  # Змініть '/tmp/ttyV1' на ваш порт
time.sleep(2)  # Чекаємо, щоб порт відкрився

try:
    while True:
        # Введення даних для відправлення
        message = input("Введіть повідомлення: ")
        ser.write((message + '\n').encode())  # Відправка повідомлення
        time.sleep(0.1)  # Додайте затримку перед читанням

        # Читання відповіді
        response = ser.readline().decode().strip()
        print("Отримано відповідь:", response)

except KeyboardInterrupt:
    print("Вихід з програми.")

finally:
    ser.close() 
