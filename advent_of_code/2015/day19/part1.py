from .shared import parse_input, generate_possibilities


def calculate(text: str) -> int:
    replacements, formula = parse_input(text)
    possibilities = set(generate_possibilities(formula, replacements))
    return len(possibilities)


puzzle = """
H => HO
H => OH
O => HH

HOH
""".strip()
assert calculate(puzzle) == 4

puzzle = """
H => HO
H => OH
O => HH

HOHOHO
""".strip()
assert calculate(puzzle) == 7
