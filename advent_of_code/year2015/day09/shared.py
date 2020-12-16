import re

from itertools import permutations
from typing import Dict, Tuple


RE_LINE = re.compile(r"(\w+) to (\w+) = (\d+)")
Distances = Dict[Tuple[str, str], int]


def parse_lines(text: str) -> Distances:
    distances = {}
    for line in text.splitlines():
        m = RE_LINE.match(line)
        if m is None:
            raise ValueError()

        a, b = m.group(1), m.group(2)
        dist = int(m.group(3))
        # add both a-b and b-a
        distances[(a, b)] = dist
        distances[(b, a)] = dist
    return distances


def find_possible_routes(distances: Distances):
    possible_destinations = set(a for a, b in distances.keys()) | set(b for a, b in distances.keys())
    for combination in permutations(possible_destinations, len(possible_destinations)):
        route_paths = tuple(zip(combination, combination[1:]))
        distance = sum(distances[route] for route in route_paths)
        yield combination, distance
