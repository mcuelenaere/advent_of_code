from .shared import parse_path, manhattan_distance, Cardinal, steps_to


def calculate(text: str) -> int:
    x, y = 0, 0
    orientation = Cardinal.North
    locations_visited = {(0, 0)}
    for direction in parse_path(text):
        for (x, y), orientation in steps_to(x, y, orientation, direction):
            if (x, y) in locations_visited:
                return manhattan_distance((0, 0), (x, y))
            locations_visited.add((x, y))


assert calculate("R8, R4, R4, R8") == 4
