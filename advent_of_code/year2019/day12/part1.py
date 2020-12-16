from .shared import Moon, parse_vectors, simulate_universe


def calculate(text: str, iterations: int = 1000) -> int:
    moons = tuple(Moon(position, [0, 0, 0]) for position in parse_vectors(text))
    for _ in range(iterations):
        simulate_universe(moons)
    return sum(moon.total_energy for moon in moons)


puzzle = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
assert calculate(puzzle, 10) == 179

puzzle = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
assert calculate(puzzle, 100) == 1940
