import sys
import unittest
from unittest.mock import MagicMock, call, patch

from src.game_board import GameBoard
from src.game_session import GameSession
from src.snake import Snake
from src.terminal_display import TerminalDisplay
from src.types import Coordinate, Direction, GameStatus


class TerminalRenderingTest(unittest.TestCase):
    def test_render_loop_sets_leaveok_clears_at_start_and_controls_cursor_visibility(self) -> None:
        display = TerminalDisplay()
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (30, 40)
        # Quit immediately on first frame key read
        stdscr.getch.return_value = ord("q")

        with patch("curses.curs_set"), patch("sys.stdout.write") as mock_write, patch("sys.stdout.flush") as mock_flush:
            display._render_loop(stdscr)

        stdscr.leaveok.assert_called_once_with(True)
        stdscr.clear.assert_called_once()
        stdscr.nodelay.assert_called_once_with(True)
        stdscr.timeout.assert_called_once_with(120)

        # ANSI cursor hide on start and restore on exit
        mock_write.assert_has_calls([call("\033[?25l"), call("\033[?25h")])
        self.assertGreaterEqual(mock_flush.call_count, 2)

    def test_render_loop_restores_cursor_even_on_exception(self) -> None:
        display = TerminalDisplay()
        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (30, 40)
        stdscr.getch.side_effect = RuntimeError("unexpected render crash")

        with patch("curses.curs_set"), patch("sys.stdout.write") as mock_write, patch("sys.stdout.flush") as mock_flush:
            with self.assertRaises(RuntimeError):
                display._render_loop(stdscr)

        # Ensure cursor re-enable sequence was emitted in finally
        mock_write.assert_has_calls([call("\033[?25l"), call("\033[?25h")])
        self.assertGreaterEqual(mock_flush.call_count, 2)

    def test_draw_does_not_call_erase_and_clears_each_line_to_eol(self) -> None:
        board = GameBoard(10, 10)
        snake = Snake((Coordinate(4, 4), Coordinate(3, 4)), Direction.RIGHT)
        session = GameSession(board=board, snake=snake, initial_food=Coordinate(8, 8))
        display = TerminalDisplay(session=session)

        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (25, 25)

        display._draw(stdscr)

        # Full erase must not be called to avoid redraw flicker
        stdscr.erase.assert_not_called()

        # Each rendered line (title, top border, 10 rows, bottom border = 13 lines)
        # must call clrtoeol to prevent ghosting
        expected_line_count = 1 + 1 + board.height + 1
        self.assertEqual(stdscr.clrtoeol.call_count, expected_line_count)
        stdscr.refresh.assert_called_once()

    def test_draw_when_window_too_small_clears_to_eol(self) -> None:
        board = GameBoard(10, 10)
        display = TerminalDisplay(session=GameSession(board=board))

        stdscr = MagicMock()
        stdscr.getmaxyx.return_value = (5, 5)

        display._draw(stdscr)

        stdscr.erase.assert_not_called()
        stdscr.addstr.assert_called_once_with(0, 0, "Terminal window too small!")
        stdscr.clrtoeol.assert_called_once()
        stdscr.refresh.assert_called_once()


if __name__ == "__main__":
    unittest.main()
