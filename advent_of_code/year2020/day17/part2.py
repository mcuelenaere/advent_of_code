from .shared import parse_grid, perform_cycle


def calculate(text: str) -> int:
    grid = parse_grid(text)
    for _ in range(6):
        grid = perform_cycle(grid, enable_fourth_dimension=True)
    return len(grid)


puzzle = """.#.
..#
###"""
assert calculate(puzzle) == 848
