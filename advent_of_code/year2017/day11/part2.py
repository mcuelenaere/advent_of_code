from .shared import parse_path, path_distance


def calculate(text: str) -> int:
    x, y = 0, 0
    max_dist = 0
    for off_x, off_y in parse_path(text):
        x += off_x
        y += off_y
        max_dist = max(path_distance(x, y), max_dist)
    return max_dist
