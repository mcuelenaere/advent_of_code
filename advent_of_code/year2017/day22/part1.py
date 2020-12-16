from .shared import State, infect, parse_text


def calculate(text: str) -> int:
    infections = parse_text(text)
    return infect(infections, 10_000, [State.CLEAN, State.INFECTED])


puzzle = """
..#
#..
...
""".strip()
assert calculate(puzzle) == 5587
