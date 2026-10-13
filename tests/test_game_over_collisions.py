import unittest
from src.game_board import GameBoard
from src.game_session import GameSession
from src.snake import Snake
from src.types import Coordinate, Direction, GameStatus


class GameOverCollisionsTest(unittest.TestCase):
    def test_game_over_when_snake_crosses_board_boundary(self) -> None:
        board = GameBoard(5, 5)
        initial_segments = (Coordinate(4, 2), Coordinate(3, 2))
        snake = Snake(initial_segments, Direction.RIGHT)
        session = GameSession(board=board, snake=snake, initial_food=Coordinate(0, 0))

        session.tick()

        self.assertEqual(session.status, GameStatus.GAME_OVER)

    def test_game_over_when_snake_collides_with_own_body(self) -> None:
        board = GameBoard(10, 10)
        # Snake in a hook shape about to run into its body:
        # (2, 2) is head, moving LEFT -> next is (1, 2)
        # Body: (2, 2) -> (2, 1) -> (1, 1) -> (1, 2) -> (1, 3)
        initial_segments = (
            Coordinate(2, 2),
            Coordinate(2, 1),
            Coordinate(1, 1),
            Coordinate(1, 2),
            Coordinate(1, 3),
        )
        snake = Snake(initial_segments, Direction.LEFT)
        session = GameSession(board=board, snake=snake, initial_food=Coordinate(9, 9))

        session.tick()

        self.assertEqual(session.status, GameStatus.GAME_OVER)


if __name__ == "__main__":
    unittest.main()
