from .shared import parse_text, calculate_score
from itertools import permutations


def calculate(text: str) -> int:
    recipy = dict(parse_text(text))

    # remove calories from recipy
    for x in recipy.values():
        del x['calories']

    # bruteforce all weight combinations
    possible_weights = (w for w in permutations(range(101), len(recipy)) if sum(w) == 100)
    return max(calculate_score(recipy.values(), w) for w in possible_weights)


puzzle = """
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
""".strip()
assert calculate(puzzle) == 62842880
