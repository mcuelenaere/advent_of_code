import re
from .shared import react_polymer, POLYMER_BASE_UNITS


def calculate(text: str) -> int:
    best_reduced_polymer = None
    for base_unit in POLYMER_BASE_UNITS:
        regex = re.compile(base_unit, flags=re.IGNORECASE)
        reduced_polymer = react_polymer(regex.sub('', text))
        if best_reduced_polymer is None or len(reduced_polymer) < len(best_reduced_polymer):
            best_reduced_polymer = reduced_polymer
    return len(best_reduced_polymer)


puzzle = "dabAcCaCBAcCcaDA"
assert calculate(puzzle) == 4
