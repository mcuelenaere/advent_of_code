from itertools import product
from typing import Tuple

from .shared import Grid, Position, parse_grid


def adjacent_positions(position: Position) -> Tuple[Position, ...]:
    x, y = position
    return (
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
    )


def evolve_grid(grid: Grid) -> Grid:
    new_grid = set()
    for y, x in product(range(5), range(5)):
        is_bug = (x, y) in grid
        neighbouring_bugs = sum(1 if (x, y) in grid else 0 for x, y in adjacent_positions((x, y)))
        if is_bug and neighbouring_bugs == 1:
            new_grid.add((x, y))
        elif not is_bug and neighbouring_bugs in (1, 2):
            new_grid.add((x, y))
    return new_grid


def calculate_biodiversity_rating(grid: Grid) -> int:
    rating = 0
    for i, (y, x) in enumerate(product(range(5), range(5))):
        if (x, y) not in grid:
            continue
        rating += pow(2, i)
    return rating


def calculate(text: str) -> int:
    grid = parse_grid(text)
    seen_states = set()
    while True:
        grid = evolve_grid(grid)
        state = tuple(grid)
        if state in seen_states:
            break
        seen_states.add(state)
    return calculate_biodiversity_rating(grid)
