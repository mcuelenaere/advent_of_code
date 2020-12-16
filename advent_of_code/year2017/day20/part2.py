from collections import Counter

from .shared import parse_text


def calculate(text: str) -> int:
    particles = tuple(parse_text(text))

    # perform 1000 iterations
    for _ in range(1000):
        freq_count = Counter()
        for p in particles:
            p.tick()
            freq_count[p.position] += 1

        # remove collisions
        particles = tuple(p for p in particles if freq_count[p.position] == 1)

    return len(particles)


puzzle = """
p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>
""".strip()
assert calculate(puzzle) == 1
