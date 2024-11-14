#include <Arduino.h>
//socat -d -d pty,link=/tmp/ttyV0,mode=777 pty,link=/tmp/ttyV1,mode=777
//picocom -b 9600 -r -l /tmp/ttyV1

void setup() {
    // Ініціалізація серійного порту
    Serial.begin(9600);
}

void loop() {
    // Перевірка, чи є доступні дані на серійному порту
    if (Serial.available() > 0) {
        // Зчитування вхідних даних
        String input = Serial.readStringUntil('\n');
        Serial.print("Received: ");
        Serial.println(input);

        // Відповідь клієнту
        String response = "Echo: " + input;
        Serial.println(response);
    }
}