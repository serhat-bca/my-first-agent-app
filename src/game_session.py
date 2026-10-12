from src.game_board import GameBoard
from src.snake import Snake
from src.types import Coordinate, Direction, GameStatus


class GameSession:
    def __init__(
        self,
        board: GameBoard | None = None,
        snake: Snake | None = None,
        initial_food: Coordinate | None = None,
    ) -> None:
        self._board: GameBoard = board if board is not None else GameBoard(20, 10)
        if snake is not None:
            self._snake: Snake = snake
        else:
            center_x = self._board.width // 2
            center_y = self._board.height // 2
            initial_segments = (
                Coordinate(center_x, center_y),
                Coordinate(center_x - 1, center_y),
                Coordinate(center_x - 2, center_y),
            )
            self._snake = Snake(initial_segments, Direction.RIGHT)

        self._score: int = 0
        self._status: GameStatus = GameStatus.RUNNING

        if initial_food is not None:
            self._food: Coordinate | None = initial_food
        else:
            self._food = self._board.generate_food_coordinate(self._snake.body)

    @property
    def board(self) -> GameBoard:
        return self._board

    @property
    def snake(self) -> Snake:
        return self._snake

    @property
    def food(self) -> Coordinate | None:
        return self._food

    @property
    def score(self) -> int:
        return self._score

    @property
    def status(self) -> GameStatus:
        return self._status

    def change_direction(self, new_direction: Direction) -> bool:
        if self._status != GameStatus.RUNNING:
            return False
        return self._snake.request_direction(new_direction)

    def tick(self) -> None:
        if self._status != GameStatus.RUNNING:
            return

        next_head = self._snake.calculate_next_head()

        if not self._board.is_within_bounds(next_head):
            self._status = GameStatus.GAME_OVER
            return

        will_eat = next_head == self._food
        if self._snake.will_collide_with_body(next_head, will_grow=will_eat):
            self._status = GameStatus.GAME_OVER
            return

        self._snake.advance(will_grow=will_eat)

        if will_eat:
            self._score += 1
            self._food = self._board.generate_food_coordinate(self._snake.body)
            if self._food is None:
                self._status = GameStatus.GAME_OVER

    def quit(self) -> None:
        self._status = GameStatus.QUIT
