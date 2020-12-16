from itertools import product
from .shared import generate_grid


def calculate(text: str) -> str:
    grid_serial_number = int(text)
    grid = generate_grid(grid_serial_number)

    # bruteforce all 3x3 combinations
    max_power_level = 0
    best_square = None
    for x in range(1, 298):
        for y in range(1, 298):
            total_power_level = sum(grid[(x + i, y + j)] for i, j in product(range(3), range(3)))
            if total_power_level > max_power_level:
                max_power_level = total_power_level
                best_square = f"{x},{y}"

    return best_square


assert calculate("18") == "33,45"
assert calculate("42") == "21,61"
