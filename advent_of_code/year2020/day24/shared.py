from typing import Iterable, List, Tuple


Coordinate = Tuple[int, int]


def parse_paths(text: str) -> Iterable[List[str]]:
    for line in text.splitlines():
        path = []
        prefix = ""
        for c in line:
            if c == "s" or c == "n":
                prefix = c
            else:
                path.append(prefix + c)
                prefix = ""
        yield path


# axial coordinates
# see https://www.redblobgames.com/grids/hexagons/#coordinates-axial
DIRECTIONS = {
    "e": (1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "w": (-1, 0),
    "nw": (0, -1),
    "ne": (1, -1),
}


def move(position: Coordinate, path: Iterable[str]) -> Coordinate:
    for direction in path:
        offset = DIRECTIONS[direction]
        position = (position[0] + offset[0], position[1] + offset[1])
    return position


assert move((0, 0), ["e", "se", "w"]) == (0, 1)
assert move((0, 0), ["nw", "w", "sw", "e", "e"]) == (0, 0)


def adjacent_tiles(position: Coordinate) -> Iterable[Coordinate]:
    yield position[0] + 1, position[1]
    yield position[0], position[1] + 1
    yield position[0] - 1, position[1] + 1
    yield position[0] - 1, position[1]
    yield position[0], position[1] - 1
    yield position[0] + 1, position[1] - 1
