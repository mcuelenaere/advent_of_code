from math import pow, sqrt
from typing import Set, Tuple


Point = Tuple[float, float]


def parse_asteroid_locations(text: str) -> Set[Point]:
    asteroid_locations = set()
    for y, line in enumerate(text.splitlines()):
        for x, letter in enumerate(line):
            if letter != "#":
                continue
            asteroid_locations.add((x, y))
    return asteroid_locations


def is_point_between_points_notworking_has_bugs(line_start: Point, line_end: Point, point_to_test: Point) -> bool:
    # make sure the starting point is always smaller than the ending point
    line_start, line_end = sorted([line_start, line_end])

    if not (line_start[0] <= point_to_test[0] <= line_end[0]) or not (line_start[1] <= point_to_test[1] <= line_end[1]):
        # point is definitely not between start and end
        return False

    if line_end[0] == line_start[0]:
        # horizontal line
        assert point_to_test[0] == line_start[0]
        return True
    elif line_end[1] == line_start[1]:
        # vertical line
        assert point_to_test[1] == line_start[1]
        return True

    # slope = (y2 - y1) / (x2 - x1)
    slope = (line_end[1] - line_start[1]) / (line_end[0] - line_start[0])
    # point-slope formula: y - y1 = slope * (x - x1) <=> 0 = slope * (x - x1) - y + y1
    result = slope * (point_to_test[0] - line_start[0]) - point_to_test[1] + line_start[1]

    # don't test exactly for 0, to negate floating point inaccuracies
    return abs(result) < 1e-15


def distance(a: Point, b: Point) -> float:
    return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))


def is_point_between_points(a: Point, b: Point, c: Point) -> bool:
    # https://stackoverflow.com/a/17693146
    return (distance(a, c) + distance(b, c)) - distance(a, b) < 1e-9


def find_best_monitoring_station(asteroid_locations: Set[Point]) -> Tuple[Point, int]:
    los_cache = {}

    def calculate_line_of_sight(start: Point, end: Point) -> bool:
        start, end = sorted([start, end])
        if (start, end) not in los_cache:
            asteroids_to_test = asteroid_locations - {start, end}
            los_cache[(start, end)] = not any(
                is_point_between_points(start_asteroid, end_asteroid, test_asteroid)
                for test_asteroid in asteroids_to_test
            )
        return los_cache[(start, end)]

    asteroid_counts = {}
    for start_asteroid in asteroid_locations:
        visible_asteroids_count = 0
        for end_asteroid in asteroid_locations - {start_asteroid}:
            has_line_of_sight = calculate_line_of_sight(start_asteroid, end_asteroid)
            if has_line_of_sight:
                visible_asteroids_count += 1
        asteroid_counts[start_asteroid] = visible_asteroids_count

    return max(asteroid_counts.items(), key=lambda x: x[1])
