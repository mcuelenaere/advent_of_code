import math
import re

from collections import defaultdict
from typing import Iterable, Tuple


# NOTE: this reeks of too much boilerplate, needs optimizing
class Position(list):
    def __init__(self, x: int, y: int):
        super(Position, self).__init__((x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __add__(self, other):
        assert isinstance(other, Position)
        return Position(self[0] + other[0], self[1] + other[1])

    def __iadd__(self, other):
        assert isinstance(other, Position)
        self[0] += other[0]
        self[1] += other[1]
        return self

    def __sub__(self, other):
        assert isinstance(other, Position)
        return Position(self[0] - other[0], self[1] - other[1])

    def __mul__(self, other):
        if isinstance(other, int):
            return Position(self[0] * other, self[1] * other)
        elif isinstance(other, Position):
            return Position(self[0] * other[0], self[1] * other[1])
        else:
            raise ValueError()

    def __truediv__(self, other):
        assert isinstance(other, Position)
        return Position(self[0] / other[0], self[1] / other[1])

    def __floordiv__(self, other):
        assert isinstance(other, Position)
        return Position(self[0] // other[0], self[1] // other[1])


class Point(object):
    __slots__ = ["position", "velocity"]

    def __init__(self, position: Position, velocity: Position):
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        return f"Point(position={self.position}, velocity={self.velocity})"


RE_POINT = re.compile(r"^position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>$")


def parse_points(text: str) -> Iterable[Point]:
    for line in text.splitlines():
        m = RE_POINT.match(line)
        if m:
            yield Point(
                position=Position(int(m.group(1)), int(m.group(2))),
                velocity=Position(int(m.group(3)), int(m.group(4))),
            )


def bounding_box(points: Iterable[Point]) -> Tuple[int, int, int, int]:
    min_x = min(p.position.x for p in points)
    max_x = max(p.position.x for p in points)
    min_y = min(p.position.y for p in points)
    max_y = max(p.position.y for p in points)
    return min_x, max_x, min_y, max_y


def visualize_points(points: Iterable[Point], width: int, height: int) -> str:
    # calculate midpoint
    min_x, max_x, min_y, max_y = bounding_box(points)
    mid_point = (max_x - min_x) // 2, (max_y - min_y) // 2

    sky = defaultdict(lambda: False)
    for point in points:
        sky[
            (
                point.position.x - min_x + mid_point[0],
                point.position.y - min_y + mid_point[1],
            )
        ] = True

    s = ""
    for y in range(height):
        s += "".join("#" if sky[(x, y)] else "." for x in range(width)) + "\n"
    return s


def find_converging_window(points: Iterable[Point]) -> Tuple[int, int]:
    min_steps = math.inf
    max_steps = 0
    for point in points:
        try:
            x, y = point.position // point.velocity
        except ZeroDivisionError:
            continue
        min_steps = min(min_steps, abs(x), abs(y))
        max_steps = max(max_steps, abs(x), abs(y))
    return min_steps, max_steps


def find_point_of_convergence(points: Iterable[Point]) -> Tuple[int, Iterable[Point]]:
    # find the range in where we think the stars will converge
    min_steps, max_steps = find_converging_window(points)

    # jump to min_steps point
    for point in points:
        point.position += point.velocity * min_steps

    # try to find the point where the bounding box is minimal
    min_width = math.inf
    min_height = math.inf
    for iteration in range(min_steps, max_steps):
        for point in points:
            point.position += point.velocity

        min_x, max_x, min_y, max_y = bounding_box(points)
        stars_width = max_x - min_x
        stars_height = max_y - min_y
        if stars_width < min_width and stars_height < min_height:
            min_width = stars_width
            min_height = stars_height
        else:
            # the previous iteration was when the stars were visible in the sky, so go back one step
            for point in points:
                point.position -= point.velocity
            return iteration, points

    raise RuntimeError("could not solve the ")
