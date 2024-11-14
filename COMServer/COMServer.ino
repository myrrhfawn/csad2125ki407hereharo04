#include <Arduino.h>

// Параметри для серійного порту
//socat -d -d pty,link=/tmp/ttyV0,mode=777 pty,link=/tmp/ttyV1,mode=777
//picocom -b 9600 -r -l /tmp/ttyV1

enum GameModes { Human_vs_Human = 0, Human_vs_AI = 1, AI_vs_AI = 2 };
GameModes currentGameMode = Human_vs_Human; // За замовчуванням, режим людина проти людини

char player1Move;
char player2Move;
bool isGameActive;

void setup() {
    Serial.begin(9600);
    randomSeed(analogRead(0)); // Ініціалізація генератора випадкових чисел
    //initializeGame();
}

void loop() {
    // Перевірка, чи є доступні дані на серійному порту
    if (Serial.available() > 0) {
        // Зчитування вхідних даних
        String input = Serial.readStringUntil('\n');
        if (input == "NEW") {
            initializeGame();
            Serial.println("Game started. Select game mode (0 for Human_vs_Human, 1 for Human_vs_AI, 2 for AI_vs_AI).");
        } else if (input.startsWith("MODE")) {
            setGameMode(input);
        } else if (input.startsWith("MOVE")) {
            handleMove(input);
        // Якщо режим AI_vs_AI активний, одразу генеруємо ходи для обох гравців
        if (currentGameMode == AI_vs_AI && isGameActive) {
            player1Move = getRandomMove();
            player2Move = getRandomMove();
            Serial.print("Player 1 (AI) has randomly chosen: ");
            Serial.println(player1Move);
            Serial.print("Player 2 (AI) has randomly chosen: ");
            Serial.println(player2Move);
            determineWinner();
            isGameActive = false;
        }
        Serial.println("end");
    }
}

void initializeGame() {
    player1Move = '\0';
    player2Move = '\0';
    isGameActive = true;
    Serial.println("New game initialized. Players can start making their moves.");
}

void setGameMode(String input) {
    // Очікується формат команди "MODE X", де X - номер режиму (0, 1 або 2)
    int mode = input.charAt(5) - '0';

    if (mode >= 0 && mode <= 2) {
        currentGameMode = static_cast<GameModes>(mode);
        Serial.print("Game mode set to: ");
        if (currentGameMode == Human_vs_Human) {
            Serial.println("Human_vs_Human");
        } else if (currentGameMode == Human_vs_AI) {
            Serial.println("Human_vs_AI");
        } else if (currentGameMode == AI_vs_AI) {
            Serial.println("AI_vs_AI");
        }
    } else {
        Serial.println("Invalid game mode. Use 0 for Human_vs_Human, 1 for Human_vs_AI, 2 for AI_vs_AI.");
    }
}

void handleMove(String input) {
    // Очікується формат команди типу "MOVE 1 R" або "MOVE 2 P"
    int player = input.charAt(5) - '0';
    char move = input.charAt(7);

    // Перевірка на правильність введеного ходу
    if (move != 'R' && move != 'P' && move != 'S') {
        Serial.println("Invalid move. Use R for Rock, P for Paper, S for Scissors.");
        return;
    }

    if (player == 1) {
        player1Move = move;
        Serial.println("Player 1 has made a move.");
    } else if (player == 2) {
        player2Move = move;
        Serial.println("Player 2 has made a move.");
    } else {
        Serial.println("Invalid player number. Use 1 or 2.");
        return;
    }

    // Якщо гравець 1 — людина, а гравець 2 — AI, то генеруємо хід для AI
    if (currentGameMode == Human_vs_AI && player1Move != '\0' && player2Move == '\0') {
        player2Move = getRandomMove();
        Serial.print("Player 2 (AI) has randomly chosen: ");
        Serial.println(player2Move);
    }

    // Якщо обидва гравці зробили свої ходи, визначити результат
    if (player1Move != '\0' && player2Move != '\0') {
        determineWinner();
        isGameActive = false; // Гра завершується після визначення переможця
    }
}

void determineWinner() {
    if (player1Move == player2Move) {
        Serial.println("It's a draw! Both players chose the same move.");
    } else if ((player1Move == 'R' && player2Move == 'S') ||
               (player1Move == 'P' && player2Move == 'R') ||
               (player1Move == 'S' && player2Move == 'P')) {
        Serial.println("Player 1 wins!");
    } else {
        Serial.println("Player 2 wins!");
    }
    initializeGame();
}

char getRandomMove() {
    int randomValue = random(0, 3); // Генеруємо випадкове число від 0 до 2
    switch (randomValue) {
        case 0:
            return 'R'; // Камінь
        case 1:
            return 'P'; // Папір
        case 2:
            return 'S'; // Ножиці
    }
    return 'R'; // Повертаємо камінь за замовчуванням (цей рядок ніколи не виконається)
}
