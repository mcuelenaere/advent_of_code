from .shared import parse_puzzle, simulate_step
from itertools import chain


def calculate(text: str, number_of_steps: int = 100) -> int:
    lights = parse_puzzle(text)
    for _ in range(number_of_steps):
        lights = simulate_step(lights)
    return sum(chain.from_iterable(lights))


puzzle = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""".strip()
assert calculate(puzzle, number_of_steps=4) == 4
