from .shared import parse_path, path_distance


def calculate(text: str) -> int:
    x, y = 0, 0
    for off_x, off_y in parse_path(text):
        x += off_x
        y += off_y
    return path_distance(x, y)


assert calculate("ne,ne,ne") == 3
assert calculate("ne,ne,sw,sw") == 0
assert calculate("ne,ne,s,s") == 2
assert calculate("se,sw,se,sw,sw") == 3
