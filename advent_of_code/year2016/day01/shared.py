from enum import Enum
from typing import Iterable, NamedTuple, Tuple


class Rotation(Enum):
    Left = "L"
    Right = "R"


class Cardinal(Enum):
    North = "N"
    East = "E"
    South = "S"
    West = "W"


Direction = NamedTuple("Direction", rotation=Rotation, blocks=int)


def parse_path(text: str):
    for part in text.split(", "):
        rotation, blocks = part[:1], part[1:]
        yield Direction(
            rotation=Rotation.Left if rotation == "L" else Rotation.Right,
            blocks=int(blocks),
        )


def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


CARDINAL_POINTS = [Cardinal.North, Cardinal.East, Cardinal.South, Cardinal.West]
VECTORS = {
    Cardinal.North: (0, -1),
    Cardinal.East: (1, 0),
    Cardinal.South: (0, 1),
    Cardinal.West: (-1, 0),
}


def steps_to(x: int, y: int, orientation: Cardinal, direction: Direction) -> Iterable[Tuple[Tuple[int, int], Cardinal]]:
    # determine new orientation
    if direction.rotation == Rotation.Left:
        orientation = CARDINAL_POINTS[(CARDINAL_POINTS.index(orientation) - 1) % len(CARDINAL_POINTS)]
    elif direction.rotation == Rotation.Right:
        orientation = CARDINAL_POINTS[(CARDINAL_POINTS.index(orientation) + 1) % len(CARDINAL_POINTS)]

    # move position
    x_off, y_off = VECTORS[orientation]
    for i in range(0, direction.blocks):
        x += x_off
        y += y_off
        yield (x, y), orientation


def move_to(x: int, y: int, orientation: Cardinal, direction: Direction) -> Tuple[Tuple[int, int], Cardinal]:
    return tuple(steps_to(x, y, orientation, direction))[-1]
