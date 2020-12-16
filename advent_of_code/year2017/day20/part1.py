from .shared import parse_text, manhattan_distance


def calculate(text: str) -> int:
    particles = tuple(parse_text(text))

    # perform 1000 iterations
    for _ in range(1000):
        for p in particles:
            p.tick()

    # find the particle closest to (0, 0, 0)
    min_distance = min(manhattan_distance(p) for p in particles)
    return next(i for i, p in enumerate(particles) if manhattan_distance(p) == min_distance)


puzzle = """
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
""".strip()
assert calculate(puzzle) == 0
