from typing import Sequence, Iterable, Tuple


class Action(object):
    North = 'N'
    South = 'S'
    East = 'E'
    West = 'W'
    Left = 'L'
    Right = 'R'
    Forward = 'F'


DIRECTION_MAP = {
    Action.North: (0, 1),
    Action.East: (1, 0),
    Action.South: (0, -1),
    Action.West: (-1, 0)
}


def parse_instructions(text: str) -> Iterable[Tuple[str, int]]:
    for line in text.splitlines():
        yield line[0], int(line[1:])


def manhattan_distance(a: Sequence[int], b: Sequence[int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
