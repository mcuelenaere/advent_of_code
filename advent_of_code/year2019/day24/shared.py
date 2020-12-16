from typing import Tuple, Set

Position = Tuple[int, int]
Grid = Set[Position]

IndexedPosition = Tuple[int, int, int]
RecursiveGrid = Set[IndexedPosition]


def parse_grid(text: str) -> Grid:
    grid = set()
    for y, line in enumerate(text.splitlines()):
        for x, char in enumerate(line):
            if char == '#':
                grid.add((x, y))
            elif char == '.':
                pass
            else:
                raise RuntimeError(f'unknown character "{char}"')
    return grid


def parse_recursive_grid(text: str) -> RecursiveGrid:
    return set((0, x, y) for x, y in parse_grid(text))
