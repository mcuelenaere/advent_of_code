from .shared import Coordinate, follow_directions, parse_directions


KEYPAD = {
    Coordinate(0, 0): 1,
    Coordinate(1, 0): 2,
    Coordinate(2, 0): 3,
    Coordinate(0, 1): 4,
    Coordinate(1, 1): 5,
    Coordinate(2, 1): 6,
    Coordinate(0, 2): 7,
    Coordinate(1, 2): 8,
    Coordinate(2, 2): 9,
}


def calculate(text: str) -> int:
    combination = ""
    directions_per_number = parse_directions(text)
    position = Coordinate(1, 1)  # start is 5
    for directions in directions_per_number:
        position = follow_directions(position, directions, valid_options=set(KEYPAD.keys()))
        combination += str(KEYPAD[position])
    return int(combination)


puzzle = """
ULL
RRDDD
LURDL
UUUUD
""".strip()
assert calculate(puzzle) == 1985
