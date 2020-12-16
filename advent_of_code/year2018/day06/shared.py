from typing import NamedTuple, Iterable, Callable


Coordinate = NamedTuple('Coordinate', x=int, y=int)


def parse_coordinates(text: str) -> Iterable[Coordinate]:
    for line in text.splitlines():
        x, y = line.split(', ', 2)
        yield Coordinate(x=int(x), y=int(y))


def manhattan_distance(p1: Coordinate, p2: Coordinate) -> int:
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)


def find_surrounded_coordinates(coordinates: Iterable[Coordinate]) -> Iterable[Coordinate]:
    surrounded_points = set()

    for c1 in coordinates:
        has_left = False
        has_right = False
        has_above = False
        has_below = False
        for c2 in coordinates:
            if c1 == c2:
                continue

            if c2.x > c1.x:
                has_right = True
            if c2.x < c1.x:
                has_left = True
            if c2.y > c1.y:
                has_below = True
            if c2.y < c1.y:
                has_above = True

            if has_left and has_right and has_above and has_below:
                break

        if has_left and has_right and has_above and has_below:
            surrounded_points.add(c1)

    return surrounded_points


def fill_grid(coordinates: Iterable[Coordinate], fn: Callable):
    min_x = min(x for x, _ in coordinates)
    max_x = max(x for x, _ in coordinates)
    min_y = min(y for _, y in coordinates)
    max_y = max(y for _, y in coordinates)

    grid = {}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            grid[(x, y)] = fn(Coordinate(x=x, y=y))

    return grid
