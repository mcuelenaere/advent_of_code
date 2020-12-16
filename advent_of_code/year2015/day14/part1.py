from .shared import calculate_distance_for, parse_text


def calculate(text: str) -> int:
    reindeers = parse_text(text)
    return max(calculate_distance_for(props, 2503) for props in reindeers.values())


puzzle = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
""".strip()
reindeers = parse_text(puzzle)
assert calculate_distance_for(reindeers["Comet"], 1000) == 1120
assert calculate_distance_for(reindeers["Dancer"], 1000) == 1056
