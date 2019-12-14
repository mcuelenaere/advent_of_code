from .shared import parse_asteroid_locations, find_best_monitoring_station, Point, distance
from math import atan2, degrees
from typing import Set, Iterable


def shoot_asteroids(asteroid_locations: Set[Point], monitoring_station: Point) -> Iterable[Point]:
    # calculate angle & distance for every target
    targets = set()
    for location in asteroid_locations:
        x = location[0] - monitoring_station[0]
        y = location[1] - monitoring_station[1]
        angle = atan2(y, x)
        angle = degrees(angle) + 90
        if angle < 0:
            angle += 360
        d = distance(location, monitoring_station)
        targets.add((location, d, angle))

    # iterate over them, clock-wise
    cur_angle = -1
    while len(targets) > 0:
        filtered = (target for target in targets if target[2] > cur_angle)
        best = min(filtered, key=lambda x: (x[2], x[1]))
        yield best[0]

        cur_angle = best[2]
        if cur_angle >= 360:
            # handle wrap-around
            cur_angle -= 360

        targets.remove(best)


def calculate(text: str) -> int:
    asteroid_locations = parse_asteroid_locations(text)
    monitoring_station, _ = find_best_monitoring_station(asteroid_locations)

    for idx, pos in enumerate(shoot_asteroids(asteroid_locations, monitoring_station)):
        if idx + 1 == 200:
            return int(pos[0] * 100 + pos[1])


puzzle = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
assert calculate(puzzle) == 802
