from .shared import drip, parse_clay


def calculate(text: str) -> int:
    clay = parse_clay(text)
    matrix = {coordinate: "#" for coordinate in clay}
    y_min = min(y for _, y in matrix.keys())

    matrix[(500, y_min - 1)] = "+"
    drip(matrix, (500, y_min - 1))

    return sum(1 for v in matrix.values() if v in ("|", "~"))


puzzle = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".strip()
assert calculate(puzzle) == 57
