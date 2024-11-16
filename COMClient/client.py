import re
import serial
import time
import os

from attr import dataclass
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

# Load settings from the .env file
load_dotenv()
SERIAL_PORT: str = os.getenv("SERIAL_PORT")
LOCAL_DIR: str = os.getenv("LOCAL_DIR")
print(f"Loaded SERIAL_PORT: {SERIAL_PORT}")
print(f"Loaded LOCAL_DIR: {LOCAL_DIR}")
BAUDRATE: int = 9600



@dataclass
class Game:
    mode: int = 0
    player1: str = ""
    player2: str = ""
    winner: str = ""

    def __str__(self):
        return f"Game(Mode[{self.mode}]: {self.player1} vs {self.player2} -> {self.winner})"


class XMLLogger:
    """
    @class XMLLogger
    @brief Class for logging game data to an XML file.

    The XMLLogger class is responsible for maintaining game logs by writing
    game information to an XML file. This includes starting new games, setting game mode,
    tracking player moves, and logging game results.

    @param file_name The name of the XML log file. Defaults to "game_log.xml".
    """

    def __init__(self, file_name: str = "game_log.xml"):
        """
        @brief Constructor to initialize the XMLLogger object.

        Initializes the XML file, creates a root element if it doesn't exist,
        and sets up necessary properties for logging games.

        @param file_name The name of the XML log file.
        """
        if LOCAL_DIR is not None and os.path.exists(LOCAL_DIR):
            self.file_path = os.path.join(LOCAL_DIR, "csad2125ki407hereharo04", file_name)
        else:
            self.file_path = os.path.join(os.getcwd(), file_name)

        self.id = 0
        self.current_game: Game = Game()
        if not os.path.exists(self.file_path):
            root = ET.Element("GameLog")
            tree = ET.ElementTree(root)
            tree.write(self.file_path)

    def process_result(self, command, response):
        """
        @brief Processes the game command and response.

        Handles game commands such as starting new games, setting game modes,
        recording player moves, and determining the winner from the response.

        @param command The command string to process.
        @param response The response string to analyze.
        """
        if "NEW" in command:
            self.id += 1
            self.current_game = Game()
        elif "MODE" in command:
            self.current_game.mode = int(command[5])
        elif "MOVE" in command:
            if command[5] == "1":
                self.current_game.player1 = command[7]
            if command[5] == "2":
                self.current_game.player2 = command[7]
        if "wins" in response or "draw" in response:
            winner_id = self.extract_winner(response)
            if winner_id is not None:
                self.current_game.winner = f"Player_{winner_id}"
            else:
                self.current_game.winner = f"draw"
            move_1, move_2 = self.extract_move(response)
            if move_1 is not None:
                self.current_game.player1 = move_2
            if move_2 is not None:
                self.current_game.player1 = move_2

            self.write_game()
            self.current_game = Game()
            self.id += 1

    def extract_winner(self, response):
        """
        @brief Extracts the winner information from the game response.

        Uses regex to determine the winner from the response string.

        @param response The response string to analyze.
        @return The winner's ID or None if not found.
        """
        winner_match = re.search(r"Player\s(\d+)\swins!", response)
        if winner_match:
            winner_id = int(winner_match.group(1))  # Extract the winner's ID
            return winner_id
        return None

    def extract_move(self, response):
        """
        @brief Extracts player moves from the response string.

        Uses regex to find the moves of player 1 and player 2 in the response.

        @param response The response string to analyze.
        @return A tuple containing moves of player 1 and player 2.
        """
        move_match = re.search(r"Player 1 .*chosen:\s([RPS])", response)
        move_1, move_2 = None, None
        if move_match:
            move_1 = move_match.group(1)  # Extract move (R, P, or S)
        move_match2 = re.search(r"Player 2 .*chosen:\s([RPS])", response)
        if move_match2:
            move_2 = move_match2.group(1)  # Extract move (R, P, or S)
        return move_1, move_2

    def write_game(self):
        """
        @brief Writes the current game data to the XML log file.

        Parses the XML file, appends the current game data as a new element,
        and writes the updated XML file to disk.
        """
        if os.path.exists(self.file_path):
            tree = ET.parse(self.file_path)
            root = tree.getroot()

            # Add a new element with the game command and result
            game = ET.Element(f"game_id_{self.id}")
            time_element = ET.SubElement(game, "timestamp")
            time_element.text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            mode_element = ET.SubElement(game, "mode")
            mode_element.text = str(self.current_game.mode)

            player1_element = ET.SubElement(game, "player1_move")
            player1_element.text = self.current_game.player1
            player2_element = ET.SubElement(game, "player2_move")
            player2_element.text = self.current_game.player2

            player2_element = ET.SubElement(game, "winner")
            player2_element.text = self.current_game.winner
            # print(f"Game [{self.id}] written: {self.current_game}")
            root.append(game)
            tree.write(self.file_path)
        else:
            print("Log file not found")

logger = XMLLogger(file_name="game_log.xml")


# Function to send commands to Arduino
def send_command(ser, command, timeout=5):
    """
    @brief Sends a command to the Arduino and logs the response.

    Writes the command to the serial port, waits for the response, and logs the response.

    @param command The command string to be sent to Arduino.
    """
    ser.write((command + '\n').encode())
    start_time = time.time()
    time.sleep(0.1)
    response = "\n"
    while True:
        msg = ser.readline().decode().strip()
        if msg == 'end' or (time.time() - start_time > timeout):
            break
        else:
            response += msg + '\n'
    print("Server response:", response)
    logger.process_result(command, response)


if __name__ == "__main__":
    """
    @brief Main entry point of the program.

    The main function initializes the menu, accepts user commands, and processes them 
    until the user exits the program. Commands are sent to the connected Arduino device, 
    and the responses are logged accordingly.
    """

    # Initialize the serial port
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)
    time.sleep(2)

    try:
        # Menu options, including selecting game mode
        print("\nMenu:")
        print("NEW - Start a new game")
        print("MODE X - Select game mode (0 for Human_vs_Human, 1 for Human_vs_AI, 2 for AI_vs_AI)")
        print("MOVE x M - Make a move (x: player number [1 or 2], M: move [R, P, S])")
        print("STATUS - Get game status")

        while True:
            # Reading the command entered by the user
            command = input("Enter command: ")

            # Sending the command to Arduino and printing the response
            send_command(ser, command)

    except KeyboardInterrupt:
        """
        @brief Handles program termination by user.

        Catches the `KeyboardInterrupt` exception (Ctrl+C) to exit the program safely.
        """
        print("Exiting the program.")

    finally:
        """
        @brief Closes the serial connection.

        Ensures that the serial port is closed properly to prevent connection issues.
        """
        ser.close()