from itertools import product
from typing import List


LightConfiguration = List[List[bool]]


def parse_puzzle(text: str) -> LightConfiguration:
    lines = text.splitlines()
    return list(list(c == "#" for c in line) for line in lines)


def simulate_step(lights: LightConfiguration) -> LightConfiguration:
    # bruteforce approach
    def is_light_on(x, y):
        if x < 0 or x >= len(lights):
            return False
        elif y < 0 or y >= len(lights):
            return False
        else:
            return lights[y][x]

    def get_neighbours_count(x, y):
        return sum(
            (
                is_light_on(x - 1, y - 1),
                is_light_on(x, y - 1),
                is_light_on(x + 1, y - 1),
                is_light_on(x + 1, y),
                is_light_on(x + 1, y + 1),
                is_light_on(x, y + 1),
                is_light_on(x - 1, y + 1),
                is_light_on(x - 1, y),
            )
        )

    new_config = [[False] * len(lights) for _ in range(len(lights))]
    for (x, y) in product(range(len(lights)), repeat=2):
        if is_light_on(x, y):
            new_config[y][x] = get_neighbours_count(x, y) in (2, 3)
        else:
            new_config[y][x] = get_neighbours_count(x, y) == 3
    return new_config
