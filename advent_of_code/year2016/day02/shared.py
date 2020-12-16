from enum import Enum
from typing import Tuple, Iterable, Set


class Coordinate(tuple):
    def __new__(cls, a: int, b: int):
        return super(Coordinate, cls).__new__(Coordinate, (a, b))

    def __add__(self, other):
        assert isinstance(other, Coordinate)
        return Coordinate(self[0] + other[0], self[1] + other[1])


class Direction(Enum):
    Left = Coordinate(-1, 0)
    Right = Coordinate(1, 0)
    Up = Coordinate(0, -1)
    Down = Coordinate(0, 1)


Directions = Tuple[Direction, ...]


def parse_directions(text: str) -> Iterable[Directions]:
    mapping = {
        'D': Direction.Down,
        'U': Direction.Up,
        'L': Direction.Left,
        'R': Direction.Right,
    }
    for line in text.splitlines():
        yield tuple(mapping[d] for d in line)


def follow_directions(start: Coordinate, directions: Directions, valid_options: Set[Coordinate]) -> Coordinate:
    position = start
    for direction in directions:
        new_position = position + direction.value
        if new_position not in valid_options:
            continue
        position = new_position
    return Coordinate(position[0], position[1])
