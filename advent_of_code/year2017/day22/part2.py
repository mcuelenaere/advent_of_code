from .shared import State, infect, parse_text


def calculate(text: str) -> int:
    infections = parse_text(text)
    return infect(
        infections,
        10_000_000,
        [State.CLEAN, State.WEAKENED, State.INFECTED, State.FLAGGED],
    )


puzzle = """
..#
#..
...
""".strip()
assert calculate(puzzle) == 2511944
