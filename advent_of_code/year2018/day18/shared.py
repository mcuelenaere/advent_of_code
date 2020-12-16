from collections import defaultdict
from typing import Dict, Iterable, Tuple


ACRE_OPEN_GROUND = "."
ACRE_TREE = "|"
ACRE_LUMBERYARD = "#"
LumberArea = Dict[Tuple[int, int], str]


def parse_lumber_area(text: str) -> LumberArea:
    area = {}
    for y, line in enumerate(text.splitlines()):
        for x, acre in enumerate(line):
            area[(x, y)] = acre
    return area


def freq_count(items: Iterable[str]) -> Dict[str, int]:
    cnt = defaultdict(int)
    for item in items:
        cnt[item] += 1
    return cnt


ADJACENT_OFFSETS = (
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
)


def advance_lumber_area(area: LumberArea) -> LumberArea:
    new_area = {}
    for (x, y), acre in area.items():
        adjacent_acres = (
            area[(x + x_off, y + y_off)] for x_off, y_off in ADJACENT_OFFSETS if (x + x_off, y + y_off) in area
        )
        adjacent_acre_counts = freq_count(adjacent_acres)

        if acre == ACRE_OPEN_GROUND:
            new_acre = ACRE_TREE if adjacent_acre_counts[ACRE_TREE] >= 3 else ACRE_OPEN_GROUND
        elif acre == ACRE_TREE:
            new_acre = ACRE_LUMBERYARD if adjacent_acre_counts[ACRE_LUMBERYARD] >= 3 else ACRE_TREE
        elif acre == ACRE_LUMBERYARD:
            new_acre = (
                ACRE_LUMBERYARD
                if adjacent_acre_counts[ACRE_LUMBERYARD] >= 1 and adjacent_acre_counts[ACRE_TREE] >= 1
                else ACRE_OPEN_GROUND
            )
        else:
            raise ValueError()
        new_area[(x, y)] = new_acre
    return new_area


def print_area(area: LumberArea):
    max_x = max(x for x, _ in area.keys())
    max_y = max(y for _, y in area.keys())
    for y in range(max_y + 1):
        print("".join(area[(x, y)] for x in range(max_x + 1)))
