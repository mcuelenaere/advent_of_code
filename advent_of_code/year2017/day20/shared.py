import re

from typing import Iterator


class Vector(object):
    __slots__ = ("x", "y", "z")

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __iadd__(self, other: "Vector"):
        assert isinstance(other, Vector), f"other should be a Vector, but is {type(other)}"
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Particle(object):
    __slots__ = ("position", "velocity", "acceleration")

    def __init__(self, position: Vector, velocity: Vector, acceleration: Vector):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def tick(self):
        self.velocity += self.acceleration
        self.position += self.velocity

    def __repr__(self):
        return f"Particle(p={self.position}, v={self.velocity}, a={self.acceleration})"


RE_PARTICLE = re.compile(r"^p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>$")


def parse_text(text: str) -> Iterator[Particle]:
    for line in text.splitlines():
        m = RE_PARTICLE.match(line)
        if m is None:
            raise ValueError(f"Could not parse line {line}")
        groups = tuple(map(int, m.groups()))
        yield Particle(
            position=Vector(groups[0], groups[1], groups[2]),
            velocity=Vector(groups[3], groups[4], groups[5]),
            acceleration=Vector(groups[6], groups[7], groups[8]),
        )


def manhattan_distance(particle: Particle) -> int:
    return sum(map(abs, particle.position))
