from itertools import permutations

from .shared import calculate_score, parse_text


def calculate(text: str) -> int:
    recipy = dict(parse_text(text))

    # remove calories from recipy
    recipy_without_calories = {k: v.copy() for k, v in parse_text(text)}
    for x in recipy_without_calories.values():
        del x["calories"]

    def calorie_count(weights):
        return sum(x["calories"] * w for x, w in zip(recipy.values(), weights))

    # bruteforce all weight combinations
    possible_weights = (
        w for w in permutations(range(101), len(recipy_without_calories)) if sum(w) == 100 and calorie_count(w) == 500
    )
    return max(calculate_score(recipy_without_calories.values(), w) for w in possible_weights)


puzzle = """
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
""".strip()
assert calculate(puzzle) == 57600000
