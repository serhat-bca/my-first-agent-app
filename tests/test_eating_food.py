import unittest
from src.game_board import GameBoard
from src.game_session import GameSession
from src.snake import Snake
from src.types import Coordinate, Direction


class EatingFoodTest(unittest.TestCase):
    def test_eating_food_grows_snake_increases_score_and_spawns_new_food(self) -> None:
        board = GameBoard(5, 5)
        initial_segments = (Coordinate(2, 2), Coordinate(1, 2))
        snake = Snake(initial_segments, Direction.RIGHT)
        food_coordinate = Coordinate(3, 2)
        session = GameSession(board=board, snake=snake, initial_food=food_coordinate)

        initial_length = len(session.snake.body)
        initial_score = session.score

        session.tick()

        self.assertEqual(session.snake.head, food_coordinate)
        self.assertEqual(len(session.snake.body), initial_length + 1)
        self.assertEqual(session.score, initial_score + 1)
        self.assertIsNotNone(session.food)
        self.assertNotIn(session.food, session.snake.body)


if __name__ == "__main__":
    unittest.main()
