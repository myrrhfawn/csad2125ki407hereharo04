#include <Arduino.h>

// Parameters for serial communication
//socat -d -d pty,link=/tmp/ttyV0,mode=777 pty,link=/tmp/ttyV1,mode=777
//picocom -b 9600 -r -l /tmp/ttyV1

/**
 * @enum GameModes
 * @brief Defines the possible game modes for the application.
 */
enum GameModes { Human_vs_Human = 0, Human_vs_AI = 1, AI_vs_AI = 2 };

/**
 * @var GameModes currentGameMode
 * @brief The current game mode, defaulted to Human_vs_Human.
 */
GameModes currentGameMode = Human_vs_Human; // Default mode is Human vs Human

/**
 * @var char player1Move
 * @brief Stores the move made by Player 1.
 */
char player1Move;

/**
 * @var char player2Move
 * @brief Stores the move made by Player 2.
 */
char player2Move;

/**
 * @var bool isGameActive
 * @brief Tracks whether the game is currently active.
 */
bool isGameActive;

/**
 * @brief Sets up the serial communication and initializes random seed.
 *
 * The setup function is called once when the Arduino starts.
 */
void setup() {
    Serial.begin(9600);
    randomSeed(analogRead(0)); // Initialize the random number generator
}

/**
 * @brief Main loop of the Arduino application.
 *
 * Handles serial communication, processes input commands, and controls game logic.
 */
void loop() {
    // Check if there are available data in the serial port
    if (Serial.available() > 0) {
        // Read incoming data
        String input = Serial.readStringUntil('\n');
        if (input == "NEW") {
            initializeGame();
            Serial.println("Game started. Select game mode (0 for Human_vs_Human, 1 for Human_vs_AI, 2 for AI_vs_AI).");
        } else if (input.startsWith("MODE")) {
            setGameMode(input);
        } else if (input.startsWith("MOVE")) {
            handleMove(input);
        }

        // If AI_vs_AI mode is active, generate moves for both players
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

/**
 * @brief Initializes a new game.
 *
 * Resets game parameters and prints the status to the serial console.
 */
void initializeGame() {
    player1Move = '\0';
    player2Move = '\0';
    isGameActive = true;
}

/**
 * @brief Sets the game mode based on the input string.
 *
 * Expects input in the format "MODE X", where X is the mode number (0, 1, or 2).
 *
 * @param input The input string specifying the game mode.
 */
void setGameMode(String input) {
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

/**
 * @brief Handles player moves.
 *
 * Expects input in the format "MOVE x M", where x is the player number (1 or 2) and M is the move (R, P, S).
 *
 * @param input The input string specifying the move.
 */
void handleMove(String input) {
    int player = input.charAt(5) - '0';
    char move = input.charAt(7);

    // Check the validity of the move
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

    // If player 1 is human and player 2 is AI, generate a move for AI
    if (currentGameMode == Human_vs_AI && player1Move != '\0' && player2Move == '\0') {
        player2Move = getRandomMove();
        Serial.print("Player 2 (AI) has randomly chosen: ");
        Serial.println(player2Move);
    }

    // If both players have made their moves, determine the result
    if (player1Move != '\0' && player2Move != '\0') {
        determineWinner();
        isGameActive = false; // Game ends after determining the winner
    }
}

/**
 * @brief Determines the winner of the game based on player moves.
 *
 * Prints the result (draw or the winning player) to the serial console.
 */
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

/**
 * @brief Generates a random move for a player.
 *
 * The possible moves are Rock ('R'), Paper ('P'), and Scissors ('S').
 *
 * @return A character representing the move ('R', 'P', 'S').
 */
char getRandomMove() {
    int randomValue = random(0, 3); // Generate a random number between 0 and 2
    switch (randomValue) {
        case 0:
            return 'R'; // Rock
        case 1:
            return 'P'; // Paper
        case 2:
            return 'S'; // Scissors
    }
    return 'R'; // Default to Rock (this line should never be executed)
}
