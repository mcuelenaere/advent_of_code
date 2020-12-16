from .shared import DIRECTION_MAP, Action, manhattan_distance, parse_instructions


DIRECTIONS = (Action.North, Action.East, Action.South, Action.West)


def calculate(text: str) -> int:
    direction = Action.East
    position = [0, 0]
    for action, value in parse_instructions(text):
        if action in DIRECTION_MAP:
            d_x, d_y = DIRECTION_MAP[action]
            position[0] += d_x * value
            position[1] += d_y * value
        elif action in (Action.Left, Action.Right):
            value //= 90
            if action == Action.Left:
                value *= -1
            offset = (DIRECTIONS.index(direction) + value) % len(DIRECTIONS)
            direction = DIRECTIONS[offset]
        elif action == Action.Forward:
            d_x, d_y = DIRECTION_MAP[direction]
            position[0] += d_x * value
            position[1] += d_y * value
    return manhattan_distance((0, 0), position)


puzzle = """F10
N3
F7
R90
F11"""
assert calculate(puzzle) == 25
