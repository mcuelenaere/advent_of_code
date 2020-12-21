from collections import defaultdict

from .shared import build_ingredient_allergen_mapping, parse_ingredients


def calculate(text: str) -> int:
    ingredients_list = tuple(parse_ingredients(text))

    # build frequency table
    freq_table = defaultdict(int)
    for ingredients, allergens in ingredients_list:
        for ingredient in ingredients:
            freq_table[ingredient] += 1

    # build mapping of ingredients to allergens
    mapping = build_ingredient_allergen_mapping(ingredients_list)

    return sum(v for k, v in freq_table.items() if k not in mapping)


puzzle = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
assert calculate(puzzle) == 5
