from typing import Tuple, Iterable


# axial coordinates
# see https://www.redblobgames.com/grids/hexagons/#coordinates-axial
DIRECTIONAL_OFFSETS = {
    'n': [0, 1],
    'ne': [1, 0],
    'se': [1, -1],
    's': [0, -1],
    'sw': [-1, 0],
    'nw': [-1, 1],
}


def parse_path(text: str) -> Iterable[Tuple[int, int]]:
    for direction in text.split(","):
        off_x, off_y = DIRECTIONAL_OFFSETS[direction]
        yield (off_x, off_y)


# https://www.redblobgames.com/grids/hexagons/#distances
def path_distance(x: int, y: int) -> int:
    return (abs(x) + abs(y) + abs(x + y)) // 2
