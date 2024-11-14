#include <Arduino.h>
//socat -d -d pty,link=/tmp/ttyV0,mode=777 pty,link=/tmp/ttyV1,mode=777
//picocom -b 9600 -r -l /tmp/ttyV1
char board[3][3];
char currentPlayer;
bool isGameActive;

void setup() {
    Serial.begin(9600);
    initializeGame();
}


void loop() {
    // Перевірка, чи є доступні дані на серійному порту
    if (Serial.available() > 0) {
        // Зчитування вхідних даних
        String input = Serial.readStringUntil('\n');
        if (input == "NEW") {
            initializeGame();
            Serial.println("Game started.");
        } else if (input.startsWith("MOVE")) {
            handleMove(input);
        } else if (input == "SAVE") {
            saveGame();
        } else if (input == "LOAD") {
            loadGame();
        } else if (input == "STATUS") {
            sendBoard();
        }
        // Відповідь клієнту
        String response = "End: " + input;
        Serial.println(response);
    }
}

void initializeGame() {
    memset(board, '-', sizeof(board));
    currentPlayer = 'X';
    isGameActive = true;
}

void handleMove(String input) {
    int x = input.charAt(5) - '0';
    int y = input.charAt(7) - '0';
    if (board[x][y] == '-' && isGameActive) {
        board[x][y] = currentPlayer;
        checkGameStatus();
        currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
        sendBoard();
    } else {
        Serial.println("Invalid move.");
    }
}

void checkGameStatus() {
    // Перевірка переможця
    // Логіка перевірки чи гра завершена (виграш або нічиї)
}

void sendBoard() {
    for (int i = 0; i < 3; i++) {
        Serial.println(String(board[i][0]) + String(board[i][1]) + String(board[i][2]));
    }
}

void saveGame() {
    // Логіка збереження стану гри
}

void loadGame() {
    // Логіка завантаження стану гри
}