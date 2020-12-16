from itertools import permutations
from typing import Iterable, Tuple

Point = Tuple[int, int, int, int]


def parse(text: str) -> Iterable[Point]:
    for line in text.splitlines():
        points = tuple(map(int, line.split(',')))
        yield points


def manhattan_distance(a: Point, b: Point) -> int:
    s = 0
    for x, y in zip(a, b):
        s += abs(x - y)
    return s


def calculate(text: str) -> int:
    points = tuple(parse(text))

    # construct initial list of constellations
    constellations = list({p} for p in points)
    for a, b in permutations(points, 2):
        if manhattan_distance(a, b) > 3:
            continue

        constellations.append({a, b})

    # reduce until there is no more overlap
    has_changed = True
    while has_changed:
        has_changed = False
        for a_idx, a in enumerate(constellations):
            for b_idx, b in enumerate(constellations):
                if a_idx == b_idx:
                    continue

                if len(a & b) > 0:
                    a.update(b)
                    constellations.remove(b)
                    has_changed = True
                    break

    return len(constellations)


_ = """
0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0
""".strip()
assert calculate(_) == 2

_ = """
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
""".strip()
assert calculate(_) == 4

_ = """
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
""".strip()
assert calculate(_) == 3

_ = """
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
""".strip()
assert calculate(_) == 8
