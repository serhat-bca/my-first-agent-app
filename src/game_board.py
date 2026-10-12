import random
from collections.abc import Callable, Collection
from src.types import Coordinate


class InvalidBoardDimensionsError(Exception):
    pass


class GameBoard:
    def __init__(self, width: int, height: int) -> None:
        if width < 3 or height < 3:
            raise InvalidBoardDimensionsError(f"Board dimensions must be at least 3x3, got {width}x{height}.")
        self._width: int = width
        self._height: int = height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def is_within_bounds(self, coordinate: Coordinate) -> bool:
        return 0 <= coordinate.x < self._width and 0 <= coordinate.y < self._height

    def generate_food_coordinate(
        self,
        occupied_coordinates: Collection[Coordinate],
        chooser: Callable[[list[Coordinate]], Coordinate] | None = None,
    ) -> Coordinate | None:
        occupied_set = set(occupied_coordinates)
        available = [
            Coordinate(x, y)
            for y in range(self._height)
            for x in range(self._width)
            if Coordinate(x, y) not in occupied_set
        ]
        if not available:
            return None
        if chooser is not None:
            return chooser(available)
        return random.choice(available)
