from .shared import find_fewest_steps, parse_input


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
