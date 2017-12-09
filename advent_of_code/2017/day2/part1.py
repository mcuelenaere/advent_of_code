from .shared import parse_input


def calculate(text: str) -> int:
    matrix = parse_input(text)
    return sum(max(row) - min(row) for row in matrix)


puzzle = """
5	1	9	5
7	5	3
2	4	6	8
""".strip()
assert calculate(puzzle) == 18
