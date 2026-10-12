import curses
import sys
import time
from src.game_session import GameSession
from src.types import Direction, GameStatus


class TerminalDisplay:
    def __init__(self, session: GameSession | None = None) -> None:
        self._session: GameSession = session if session is not None else GameSession()

    def run(self) -> None:
        if not (sys.stdin.isatty() and sys.stdout.isatty()):
            print("Snake Game: terminal interface requires an interactive TTY.")
            print("Run directly in your terminal: python -m src")
            return

        try:
            curses.wrapper(self._render_loop)
        except curses.error as exc:
            print(f"Snake Game: could not initialize curses display ({exc}).")
            print("Run directly in your terminal: python -m src")

    def _render_loop(self, stdscr: curses.window) -> None:
        try:
            curses.curs_set(0)
        except curses.error:
            pass
        # Terminal escape code to ensure hardware cursor is invisible (supported across all terminals)
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        stdscr.leaveok(True)
        stdscr.nodelay(True)
        stdscr.timeout(120)

        # Clear once at start
        stdscr.clear()

        try:
            while self._session.status == GameStatus.RUNNING:
                key = stdscr.getch()
                self._handle_input(key)
                self._session.tick()
                self._draw(stdscr)

            if self._session.status == GameStatus.GAME_OVER:
                self._show_game_over(stdscr)
        finally:
            # Re-enable cursor when game exits
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

    def _handle_input(self, key: int) -> None:
        if key in (ord("q"), ord("Q"), 27):
            self._session.quit()
        elif key in (curses.KEY_UP, ord("w"), ord("W")):
            self._session.change_direction(Direction.UP)
        elif key in (curses.KEY_DOWN, ord("s"), ord("S")):
            self._session.change_direction(Direction.DOWN)
        elif key in (curses.KEY_LEFT, ord("a"), ord("A")):
            self._session.change_direction(Direction.LEFT)
        elif key in (curses.KEY_RIGHT, ord("d"), ord("D")):
            self._session.change_direction(Direction.RIGHT)

    def _draw(self, stdscr: curses.window) -> None:
        board = self._session.board
        max_y, max_x = stdscr.getmaxyx()

        needed_height = board.height + 4
        needed_width = board.width + 4
        if max_y < needed_height or max_x < needed_width:
            stdscr.addstr(0, 0, "Terminal window too small!")
            stdscr.clrtoeol()
            stdscr.refresh()
            return

        title = f" SNAKE | Score: {self._session.score} | Controls: WASD/Arrows, Q to quit "
        stdscr.addstr(0, 0, title)
        stdscr.clrtoeol()

        # Draw top wall
        stdscr.addstr(1, 0, "+" + "-" * board.width + "+")
        stdscr.clrtoeol()

        # Draw board content
        food = self._session.food
        snake_head = self._session.snake.head
        snake_body = set(self._session.snake.body[1:])

        for row in range(board.height):
            line_chars: list[str] = ["|"]
            for col in range(board.width):
                from src.types import Coordinate
                curr = Coordinate(col, row)
                if curr == snake_head:
                    line_chars.append("@")
                elif curr in snake_body:
                    line_chars.append("o")
                elif food is not None and curr == food:
                    line_chars.append("*")
                else:
                    line_chars.append(" ")
            line_chars.append("|")
            stdscr.addstr(row + 2, 0, "".join(line_chars))
            stdscr.clrtoeol()

        # Draw bottom wall
        stdscr.addstr(board.height + 2, 0, "+" + "-" * board.width + "+")
        stdscr.clrtoeol()
        stdscr.refresh()

    def _show_game_over(self, stdscr: curses.window) -> None:
        stdscr.nodelay(False)
        msg_1 = f"GAME OVER! Final Score: {self._session.score}"
        msg_2 = "Press Enter or Q to exit."
        board = self._session.board
        y_offset = board.height + 4
        stdscr.addstr(y_offset, 0, msg_1)
        stdscr.addstr(y_offset + 1, 0, msg_2)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key in (10, 13, ord("q"), ord("Q"), 27):
                break


def start_terminal_game() -> None:
    display = TerminalDisplay()
    display.run()
