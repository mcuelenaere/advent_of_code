import re

from typing import Dict, Set, Tuple


Coordinate = Tuple[int, int]
Matrix = Dict[Coordinate, str]

RE_CLAY_COLUMN = re.compile(r"^x=(\d+), y=(\d+)\.\.(\d+)$")
RE_CLAY_LINE = re.compile(r"^y=(\d+), x=(\d+)\.\.(\d+)$")


def parse_clay(text: str) -> Set[Coordinate]:
    coordinates = set()
    for line in text.splitlines():
        m = RE_CLAY_COLUMN.match(line)
        if m:
            x = int(m.group(1))
            y_min = int(m.group(2))
            y_max = int(m.group(3))
            for y in range(y_min, y_max + 1):
                coordinates.add((x, y))

        m = RE_CLAY_LINE.match(line)
        if m:
            y = int(m.group(1))
            x_min = int(m.group(2))
            x_max = int(m.group(3))
            for x in range(x_min, x_max + 1):
                coordinates.add((x, y))
    return coordinates


def print_matrix(m: Matrix):
    x_min = min(x for x, _ in m.keys())
    x_max = max(x for x, _ in m.keys())
    y_min = min(y for _, y in m.keys())
    y_max = max(y for _, y in m.keys())

    for y in range(y_min, y_max + 1):
        print("".join(m.get((x, y), ".") for x in range(x_min - 1, x_max + 2)))


def drip(matrix: Matrix, origin: Coordinate):
    y_max = max(y for _, y in matrix.keys())
    queue = {origin}

    def tile_at(x: int, y: int) -> str:
        return matrix.get((x, y), ".")

    def tag_as_visited(x: int, y: int):
        assert tile_at(x, y) in (".", "|")
        matrix[(x, y)] = "|"

    def tag_as_water(x: int, y: int):
        assert tile_at(x, y) in (".", "|", "~")
        matrix[(x, y)] = "~"

    while len(queue) > 0:
        pos = list(queue.pop())

        # keep going down until we are stopped
        while tile_at(pos[0], pos[1] + 1) in (".", "|") and pos[1] + 1 <= y_max:
            pos[1] += 1
            tag_as_visited(*pos)
        pos_before_dripping_down = (pos[0], pos[1] - 1)

        if pos[1] == y_max:
            # we went out of bounds
            continue

        # determine left boundary
        left_boundary = pos[0]
        while tile_at(left_boundary - 1, pos[1]) in (".", "|") and tile_at(left_boundary, pos[1] + 1) not in (".", "|"):
            tag_as_visited(left_boundary, pos[1])
            left_boundary -= 1

        if tile_at(left_boundary, pos[1]) in (".", "|"):
            tag_as_visited(left_boundary, pos[1])

        # determine right boundary
        right_boundary = pos[0]
        while tile_at(right_boundary + 1, pos[1]) in (".", "|") and tile_at(right_boundary, pos[1] + 1) not in (
            ".",
            "|",
        ):
            tag_as_visited(right_boundary, pos[1])
            right_boundary += 1

        if tile_at(right_boundary, pos[1]) in (".", "|"):
            tag_as_visited(right_boundary, pos[1])

        # check if both ends are bounded
        bounded_left_edge = tile_at(left_boundary - 1, pos[1]) not in (".", "|") and tile_at(
            left_boundary, pos[1] + 1
        ) not in (".", "|")
        bounded_right_edge = tile_at(right_boundary + 1, pos[1]) not in (".", "|") and tile_at(
            right_boundary, pos[1] + 1
        ) not in (".", "|")
        if bounded_left_edge and bounded_right_edge:
            # flood row with water
            for x in range(left_boundary, right_boundary + 1):
                tag_as_water(x, pos[1])

            # re-queue origin of drip
            queue.add(pos_before_dripping_down)
        else:
            if not bounded_left_edge:
                queue.add((left_boundary, pos[1]))
            if not bounded_right_edge:
                queue.add((right_boundary, pos[1]))
