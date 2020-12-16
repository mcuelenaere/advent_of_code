from typing import Dict, Tuple


def calculate_power_level(x: int, y: int, serial_number: int) -> int:
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    power_level = (power_level % 1000) // 100
    power_level -= 5
    return power_level


assert calculate_power_level(3, 5, 8) == 4
assert calculate_power_level(122, 79, 57) == -5
assert calculate_power_level(217, 196, 39) == 0
assert calculate_power_level(101, 153, 71) == 4


def generate_grid(grid_serial_number: int) -> Dict[Tuple[int, int], int]:
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            grid[(x, y)] = calculate_power_level(x, y, grid_serial_number)
    return grid
