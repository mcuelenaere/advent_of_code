from .shared import calculate_score, parse_text


def calculate(text: str) -> int:
    reindeers = parse_text(text)
    return calculate_score(reindeers, 2503)


puzzle = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
""".strip()
reindeers = parse_text(puzzle)
assert calculate_score(reindeers, 1000) == 689
