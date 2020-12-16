from .shared import parse_path, manhattan_distance, Cardinal, move_to


def calculate(text: str) -> int:
    x, y = 0, 0
    orientation = Cardinal.North
    for direction in parse_path(text):
        (x, y), orientation = move_to(x, y, orientation, direction)
    return manhattan_distance((0, 0), (x, y))


assert calculate("R2, L3") == 5
assert calculate("R2, R2, R2") == 2
assert calculate("R5, L5, R5, R3") == 12
