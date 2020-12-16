from itertools import product

from .shared import parse_input


def calculate(text: str) -> int:
    matrix = parse_input(text)
    s = 0
    for row in matrix:
        # bruteforce all combinations
        for a, b in product(row, repeat=2):
            if a != b and a % b == 0:
                s += a / b
                break
    return s


puzzle = """
5	9	2	8
9	4	7	3
3	8	6	5
""".strip()
assert calculate(puzzle) == 9
