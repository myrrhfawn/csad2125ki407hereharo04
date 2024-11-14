import unittest
from unittest.mock import patch, MagicMock
from your_module import XMLLogger, Game, send_command  # replace 'your_module' with actual module name


class TestGame(unittest.TestCase):
    def test_game_initialization(self):
        game = Game()
        self.assertEqual(game.mode, 0)
        self.assertEqual(game.player1, "")
        self.assertEqual(game.player2, "")
        self.assertEqual(game.winner, "")


class TestXMLLogger(unittest.TestCase):
    @patch("your_module.os.path.exists", return_value=False)
    @patch("your_module.ET.ElementTree.write")
    def test_logger_initialization_creates_file(self, mock_write, mock_exists):
        logger = XMLLogger()
        mock_write.assert_called_once()

    @patch("your_module.XMLLogger.write_game")
    def test_process_result_start_new_game(self, mock_write_game):
        logger = XMLLogger()
        logger.process_result("NEW", "")
        self.assertEqual(logger.id, 1)
        self.assertEqual(logger.current_game.mode, 0)

    @patch("your_module.XMLLogger.write_game")
    def test_process_result_set_mode(self, mock_write_game):
        logger = XMLLogger()
        logger.process_result("MODE 1", "")
        self.assertEqual(logger.current_game.mode, 1)

    def test_extract_winner(self):
        logger = XMLLogger()
        result = logger.extract_winner("Player 1 wins!")
        self.assertEqual(result, 1)
        result = logger.extract_winner("Player 2 wins!")
        self.assertEqual(result, 2)
        result = logger.extract_winner("No winner")
        self.assertIsNone(result)

    def test_extract_move(self):
        logger = XMLLogger()
        result = logger.extract_move("Player 1 has chosen: R\nPlayer 2 has chosen: P")
        self.assertEqual(result, ("R", "P"))
        result = logger.extract_move("Player 1 has chosen: S\nPlayer 2 has chosen: R")
        self.assertEqual(result, ("S", "R"))

    @patch("your_module.ET.ElementTree.write")
    def test_write_game(self, mock_write):
        logger = XMLLogger()
        logger.current_game = Game(mode=1, player1="R", player2="P", winner="Player_1")
        logger.write_game()
        mock_write.assert_called_once()


class TestSendCommand(unittest.TestCase):
    @patch("your_module.ser.write")
    @patch("your_module.ser.readline", side_effect=[b'Server response line\n', b'end\n'])
    @patch("your_module.logger.process_result")
    def test_send_command(self, mock_process_result, mock_readline, mock_write):
        send_command("TEST_COMMAND")
        mock_write.assert_called_once()
        mock_process_result.assert_called_once_with("TEST_COMMAND", "\nServer response line\n")


if __name__ == "__main__":
    unittest.main()
