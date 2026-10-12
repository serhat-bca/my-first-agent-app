import unittest
from src.game_board import GameBoard
from src.game_session import GameSession
from src.snake import Snake
from src.types import Coordinate, Direction


class SnakeMovementTest(unittest.TestCase):
    def test_snake_advances_one_cell_in_current_direction_on_tick(self) -> None:
        board = GameBoard(10, 10)
        initial_segments = (Coordinate(4, 4), Coordinate(3, 4))
        snake = Snake(initial_segments, Direction.RIGHT)
        session = GameSession(board=board, snake=snake, initial_food=Coordinate(8, 8))

        session.tick()

        self.assertEqual(session.snake.head, Coordinate(5, 4))
        self.assertEqual(session.snake.body, (Coordinate(5, 4), Coordinate(4, 4)))

    def test_snake_ignores_immediate_reverse_direction_request(self) -> None:
        board = GameBoard(10, 10)
        initial_segments = (Coordinate(4, 4), Coordinate(3, 4))
        snake = Snake(initial_segments, Direction.RIGHT)
        session = GameSession(board=board, snake=snake, initial_food=Coordinate(8, 8))

        accepted = session.change_direction(Direction.LEFT)
        self.assertFalse(accepted)

        session.tick()
        self.assertEqual(session.snake.head, Coordinate(5, 4))


if __name__ == "__main__":
    unittest.main()
