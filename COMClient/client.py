import re

import serial
import time
import os

from attr import dataclass
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

from onnxruntime.tools.ort_format_model.ort_flatbuffers_py.fbs.Node import NodeEnd

# Завантаження налаштувань з файлу .env
load_dotenv()
SERIAL_PORT: str = os.getenv("SERIAL_PORT")
LOCAL_DIR: str = os.getenv("LOCAL_DIR")
print(f"Loaded SERIAL_PORT: {SERIAL_PORT}")
print(f"Loaded LOCAL_DIR: {LOCAL_DIR}")
BAUDRATE: int = 9600

# Ініціалізація серійного порту
ser = serial.Serial(SERIAL_PORT, BAUDRATE)
time.sleep(2)

@dataclass
class Game:
    mode: int =  0
    player1: str = ""
    player2: str = ""
    winner: str = ""

    def __str__(self):
        return f"Game(Mode[{self.mode}]: {self.player1} vs {self.player2} -> {self.winner})"

class XMLLogger:
    def __init__(self, file_name: str = "game_log.xml"):
        self.file_path = os.path.join(LOCAL_DIR, "csad2125ki407hereharo04", file_name)
        self.id = 0
        self.current_game: Game = Game()
        if not os.path.exists(self.file_path):
            root = ET.Element("GameLog")
            tree = ET.ElementTree(root)
            tree.write(self.file_path)

    def process_result(self, command, response):
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
        winner_match = re.search(r"Player\s(\d+)\swins!", response)
        if winner_match:
            winner_id = int(winner_match.group(1))  # Витягуємо номер переможця
            return winner_id
        return None

    def extract_move(self, response):
        # Використовуємо регулярний вираз для знаходження номера гравця та ходу
        move_match = re.search(r"Player 1 .*chosen:\s([RPS])", response)
        move_1, move_2 = None, None
        if move_match:
            move_1 = move_match.group(1)  # Витягуємо сам хід (R, P, або S)
        move_match2 = re.search(r"Player 2 .*chosen:\s([RPS])", response)
        if move_match2:
            move_2 = move_match2.group(1)  # Витягуємо сам хід (R, P, або S)
        return move_1, move_2

    def write_game(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        # Додаємо новий елемент з даними про команду та результат
        game = ET.Element(f"game_id_{self.id}")
        time_element = ET.SubElement(game, "timestamp")
        time_element.text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        mode_element = ET.SubElement(game, "mode")
        mode_element.text = int(self.current_game.mode)

        player1_element = ET.SubElement(game, "player1_move")
        player1_element.text = self.current_game.player1
        player2_element = ET.SubElement(game, "player2_move")
        player2_element.text = self.current_game.player2

        player2_element = ET.SubElement(game, "winner")
        player2_element.text = self.current_game.winner
        print(f"Game [{self.id}] writed: {self.current_game}")
        root.append(game)
        tree.write(self.file_path)

logger = XMLLogger(file_name="game_log.xml")

# Функція для відправки команд на Arduino
def send_command(command):
    ser.write((command + '\n').encode())
    time.sleep(0.1)
    response = "\n"
    while True:
        msg = ser.readline().decode().strip()
        if msg == 'end':
            break
        else:
            response += msg + '\n'
    print("Server response:", response)
    logger.process_result(command, response)

try:
    # Меню з опціями, включаючи вибір режиму гри
    print("\nMenu:")
    print("NEW - Start a new game")
    print("MODE X - Select game mode (0 for Human_vs_Human, 1 for Human_vs_AI, 2 for AI_vs_AI)")
    print("MOVE x M - Make a move (x: player number [1 or 2], M: move [R, P, S])")
    print("STATUS - Get game status")

    while True:
        # Читання введеної користувачем команди
        command = input("Enter command: ")

        # Надсилання команди на Arduino та друк відповіді
        send_command(command)

except KeyboardInterrupt:
    print("Exiting the program.")

finally:
    ser.close()
