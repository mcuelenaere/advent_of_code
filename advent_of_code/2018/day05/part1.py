from .shared import react_polymer


def calculate(text: str) -> int:
    reacted_polymer = react_polymer(text)
    return len(reacted_polymer)


puzzle = "dabAcCaCBAcCcaDA"
assert calculate(puzzle) == 10
