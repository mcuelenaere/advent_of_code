from .shared import calculate_rows, walk_as_grid
from typing import Dict, Optional, Tuple


def flood_grid(grid: Dict[Tuple[int, int], Optional[int]], x: int, y: int, colour: int):
    def try_(x, y):
        if grid.get((x, y), -1) is not None:
            return

        grid[(x, y)] = colour
        flood_grid(grid, x, y, colour)

    # colour ourselves first
    grid[(x, y)] = colour

    # now try our neighbours
    try_(x - 1, y)  # left
    try_(x, y + 1)  # top
    try_(x + 1, y)  # right
    try_(x, y - 1)  # bottom


def calculate(text: str) -> int:
    rows = calculate_rows(text)
    grid = {(x, y): None for x, y, is_set in walk_as_grid(rows) if is_set}

    counter = 1
    for (x, y), colour in grid.items():
        if colour is not None:
            continue

        flood_grid(grid, x, y, counter)
        counter += 1

    return len(set(grid.values()))


assert calculate('flqrgnkx') == 1242
