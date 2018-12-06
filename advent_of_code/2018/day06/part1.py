from collections import defaultdict
from .shared import parse_coordinates, find_surrounded_coordinates, fill_grid, manhattan_distance


def calculate(text: str) -> int:
    coordinates = tuple(parse_coordinates(text))
    labeled_coordinates = {chr(65 + i): c for i, c in enumerate(coordinates)}

    def cb(c):
        min_dist = None
        min_labels = set()
        for label, o in labeled_coordinates.items():
            dist = manhattan_distance(c, o)
            if min_dist is None or dist < min_dist:
                # new winner
                min_dist = dist
                min_labels = {label}
            elif dist == min_dist:
                # equal distances
                min_labels.add(label)

        return tuple(min_labels)[0] if len(min_labels) == 1 else '.'
    grid = fill_grid(coordinates, cb)

    # do a simple frequency count
    areas_by_label = defaultdict(lambda: 0)
    for label in grid.values():
        areas_by_label[label] += 1

    # determine which labels are not infinite
    surrounded_coordinates = set(find_surrounded_coordinates(coordinates))
    labels_to_look_for = tuple(l for l, c in labeled_coordinates.items() if c in surrounded_coordinates)

    # find the max areas
    return max(areas_by_label[i] for i in labels_to_look_for)


puzzle = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".strip()
assert calculate(puzzle) == 17
