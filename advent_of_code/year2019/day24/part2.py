from itertools import product
from typing import Tuple

from .shared import IndexedPosition, RecursiveGrid, parse_recursive_grid


def adjacent_positions(position: IndexedPosition) -> Tuple[IndexedPosition, ...]:
    idx, x, y = position
    if (x, y) == (2, 2):
        # center tile
        raise ValueError("cannot calculate adjacent positions for center")

    adjacent = {
        (idx, x, y - 1),
        (idx, x + 1, y),
        (idx, x, y + 1),
        (idx, x - 1, y),
    }

    if (x, y) == (2, 1):
        # top tile
        adjacent.remove((idx, 2, 2))
        adjacent.update((idx - 1, x, 0) for x in range(5))
    elif (x, y) == (3, 2):
        # right tile
        adjacent.remove((idx, 2, 2))
        adjacent.update((idx - 1, 4, y) for y in range(5))
    elif (x, y) == (2, 3):
        # bottom tile
        adjacent.remove((idx, 2, 2))
        adjacent.update((idx - 1, x, 4) for x in range(5))
    elif (x, y) == (1, 2):
        # left tile
        adjacent.remove((idx, 2, 2))
        adjacent.update((idx - 1, 0, y) for y in range(5))

    if x == 0:
        # left row
        adjacent.remove((idx, x - 1, y))
        adjacent.add((idx + 1, 1, 2))
    elif x == 4:
        # right row
        adjacent.remove((idx, x + 1, y))
        adjacent.add((idx + 1, 3, 2))

    if y == 0:
        # top row
        adjacent.remove((idx, x, y - 1))
        adjacent.add((idx + 1, 2, 1))
    elif y == 4:
        # bottom row
        adjacent.remove((idx, x, y + 1))
        adjacent.add((idx + 1, 2, 3))

    return tuple(adjacent)


def evolve_grid(grid: RecursiveGrid) -> RecursiveGrid:
    new_grid = set()
    min_idx = min(idx for idx, _, _ in grid) - 1
    max_idx = max(idx for idx, _, _ in grid) + 1
    for idx, y, x in product(range(min_idx, max_idx + 1), range(5), range(5)):
        if (x, y) == (2, 2):
            continue

        is_bug = (idx, x, y) in grid
        neighbouring_bugs = sum(1 if (idx, x, y) in grid else 0 for idx, x, y in adjacent_positions((idx, x, y)))
        if is_bug and neighbouring_bugs == 1:
            new_grid.add((idx, x, y))
        elif not is_bug and neighbouring_bugs in (1, 2):
            new_grid.add((idx, x, y))
    return new_grid


def calculate(text: str) -> int:
    grid = parse_recursive_grid(text)
    for _ in range(200):
        grid = evolve_grid(grid)
    return len(grid)
