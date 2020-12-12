from .shared import parse_instructions, Action, manhattan_distance, DIRECTION_MAP


def calculate(text: str) -> int:
    position = [0, 0]
    waypoint = [10, 1]
    for action, value in parse_instructions(text):
        if action in DIRECTION_MAP:
            d_x, d_y = DIRECTION_MAP[action]
            waypoint[0] += d_x * value
            waypoint[1] += d_y * value
        elif action == Action.Right:
            while value > 0:
                waypoint[0], waypoint[1] = waypoint[1], -waypoint[0]
                value -= 90
        elif action == Action.Left:
            while value > 0:
                waypoint[0], waypoint[1] = -waypoint[1], waypoint[0]
                value -= 90
        elif action == Action.Forward:
            position[0] += waypoint[0] * value
            position[1] += waypoint[1] * value
    return manhattan_distance((0, 0), position)


puzzle = """F10
N3
F7
R90
F11"""
assert calculate(puzzle) == 286
