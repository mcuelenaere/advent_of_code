from .shared import parse_input, find_fewest_steps


def calculate(text: str) -> int:
    replacements, outcome = parse_input(text)
    return find_fewest_steps(outcome, replacements)


puzzle = """
e => H
e => O
H => HO
H => OH
O => HH

HOH
""".strip()
assert calculate(puzzle) == 3

puzzle = """
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
""".strip()
assert calculate(puzzle) == 6
