from collections import defaultdict

from .shared import execute_instruction, parse_instructions


def calculate(text: str, width: int = 50, height: int = 6) -> int:
    matrix = defaultdict(lambda: False)
    for instruction in parse_instructions(text):
        execute_instruction(matrix, width, height, instruction)
    return sum(1 for lit in matrix.values() if lit)


puzzle = """
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
""".strip()
assert calculate(puzzle, width=7, height=3) == 6
