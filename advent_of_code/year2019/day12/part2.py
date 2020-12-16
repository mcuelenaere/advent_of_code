from math import gcd

from .shared import Moon, parse_vectors, simulate_universe


def lcm(a, b):
    # https://stackoverflow.com/a/51716959
    return abs(a * b) // gcd(a, b)


def calculate(text: str) -> int:
    moons = tuple(Moon(position, [0, 0, 0]) for position in parse_vectors(text))

    # simulate universes until we've found cycles for all the axises
    states = (set(), set(), set())
    cycles = [None, None, None]
    counter = 0
    while any(c is None for c in cycles):
        for i in range(3):
            if cycles[i] is not None:
                # we've already found the cycle for this axis
                continue

            state = tuple((moon.velocity[i], moon.position[i]) for moon in moons)
            if state in states[i]:
                # found the cycle!
                cycles[i] = counter
            states[i].add(state)

        simulate_universe(moons)
        counter += 1

    return lcm(lcm(cycles[0], cycles[1]), cycles[2])


puzzle = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
assert calculate(puzzle) == 2772

puzzle = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
assert calculate(puzzle) == 4686774924
