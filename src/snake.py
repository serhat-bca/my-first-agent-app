from collections.abc import Sequence
from src.types import Coordinate, Direction


class InvalidSnakeError(Exception):
    pass


class Snake:
    def __init__(self, segments: Sequence[Coordinate], direction: Direction) -> None:
        if not segments:
            raise InvalidSnakeError("Snake must contain at least one segment.")
        self._body: list[Coordinate] = list(segments)
        self._direction: Direction = direction
        self._pending_direction: Direction = direction

    @property
    def body(self) -> tuple[Coordinate, ...]:
        return tuple(self._body)

    @property
    def head(self) -> Coordinate:
        return self._body[0]

    @property
    def direction(self) -> Direction:
        return self._direction

    def request_direction(self, new_direction: Direction) -> bool:
        if len(self._body) > 1 and new_direction == self._direction.opposite():
            return False
        self._pending_direction = new_direction
        return True

    def calculate_next_head(self) -> Coordinate:
        return self.head.translate(self._pending_direction)

    def will_collide_with_body(self, next_head: Coordinate, will_grow: bool = False) -> bool:
        body_to_check = self._body if will_grow else self._body[:-1]
        return next_head in body_to_check

    def advance(self, will_grow: bool = False) -> Coordinate:
        self._direction = self._pending_direction
        next_head = self.head.translate(self._direction)
        self._body.insert(0, next_head)
        if not will_grow:
            self._body.pop()
        return next_head
