from .shared import parse_coordinates, fill_grid, manhattan_distance


def calculate(text: str, max_distance: int = 10000) -> int:
    coordinates = tuple(parse_coordinates(text))

    def cb(c):
        total_distance = sum(manhattan_distance(c, o) for o in coordinates)
        if total_distance < max_distance:
            return '#'
        else:
            return '.'
    grid = fill_grid(coordinates, cb)

    return sum(1 for v in grid.values() if v == '#')


puzzle = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".strip()
assert calculate(puzzle, max_distance=32) == 16
