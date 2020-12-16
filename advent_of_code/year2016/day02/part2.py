from .shared import Coordinate, follow_directions, parse_directions


KEYPAD = {
    Coordinate(2, 0): "1",
    Coordinate(1, 1): "2",
    Coordinate(2, 1): "3",
    Coordinate(3, 1): "4",
    Coordinate(0, 2): "5",
    Coordinate(1, 2): "6",
    Coordinate(2, 2): "7",
    Coordinate(3, 2): "8",
    Coordinate(4, 2): "9",
    Coordinate(1, 3): "A",
    Coordinate(2, 3): "B",
    Coordinate(3, 3): "C",
    Coordinate(2, 4): "D",
}


def calculate(text: str) -> str:
    combination = ""
    directions_per_number = parse_directions(text)
    position = Coordinate(0, 2)  # start is 5
    for directions in directions_per_number:
        position = follow_directions(position, directions, valid_options=set(KEYPAD.keys()))
        combination += str(KEYPAD[position])
    return combination


puzzle = """
ULL
RRDDD
LURDL
UUUUD
""".strip()
assert calculate(puzzle) == "5DB3"
