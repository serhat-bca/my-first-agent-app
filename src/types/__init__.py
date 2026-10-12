"""Shared types for the whole application. Define each type once, here."""

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def opposite(self) -> "Direction":
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.RIGHT if self == Direction.RIGHT else Direction.LEFT,
        }
        opposites[Direction.LEFT] = Direction.RIGHT
        opposites[Direction.RIGHT] = Direction.LEFT
        return opposites[self]


class GameStatus(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    GAME_OVER = "GAME_OVER"
    QUIT = "QUIT"


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def translate(self, direction: Direction) -> "Coordinate":
        if direction == Direction.UP:
            return Coordinate(self.x, self.y - 1)
        if direction == Direction.DOWN:
            return Coordinate(self.x, self.y + 1)
        if direction == Direction.LEFT:
            return Coordinate(self.x - 1, self.y)
        if direction == Direction.RIGHT:
            return Coordinate(self.x + 1, self.y)
        raise ValueError(f"Unknown direction: {direction}")
