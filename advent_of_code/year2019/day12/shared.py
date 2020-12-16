import re
from itertools import combinations
from typing import List, Iterable, NamedTuple, Tuple

Vector = List[int]
RE_POSITION = re.compile(r'^\<x=(-?\d+), y=(-?\d+), z=(-?\d+)\>$')


class Moon(NamedTuple):
    position: Vector
    velocity: Vector

    @property
    def potential_energy(self):
        return sum(map(abs, self.position))

    @property
    def kinetic_energy(self):
        return sum(map(abs, self.velocity))

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy


def parse_vectors(text: str) -> Iterable[Vector]:
    for line in text.splitlines():
        m = RE_POSITION.match(line)
        if not m:
            continue
        yield [int(x) for x in m.groups()]


def simulate_universe(moons: Tuple[Moon]):
    # apply gravity
    for left, right in combinations(moons, 2):
        for i in range(3):
            if left.position[i] > right.position[i]:
                left.velocity[i] -= 1
                right.velocity[i] += 1
            elif left.position[i] < right.position[i]:
                left.velocity[i] += 1
                right.velocity[i] -= 1

    # apply velocity
    for moon in moons:
        for i in range(3):
            moon.position[i] += moon.velocity[i]
