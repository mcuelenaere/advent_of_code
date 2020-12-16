from itertools import chain

from .shared import parse_puzzle, simulate_step


def calculate(text: str, number_of_steps: int = 100) -> int:
    lights = parse_puzzle(text)
    for _ in range(number_of_steps):
        lights[0][0] = True
        lights[0][-1] = True
        lights[-1][0] = True
        lights[-1][-1] = True
        lights = simulate_step(lights)
    lights[0][0] = True
    lights[0][-1] = True
    lights[-1][0] = True
    lights[-1][-1] = True
    return sum(chain.from_iterable(lights))


puzzle = """
##.#.#
...##.
#....#
..#...
#.#..#
####.#
""".strip()
assert calculate(puzzle, number_of_steps=5) == 17
