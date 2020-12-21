import re

from collections import defaultdict
from itertools import product
from typing import Dict, Iterable, List, Tuple


RE_INGREDIENT = re.compile(r"^([\w\s]+) \(contains ([\w,\s]+)\)$")


def parse_ingredients(text: str) -> Iterable[Tuple[List[str], List[str]]]:
    for line in text.splitlines():
        m = RE_INGREDIENT.match(line)
        assert m is not None
        ingredients = m.group(1).split(" ")
        allergens = m.group(2).split(", ")
        yield ingredients, allergens


def build_ingredient_allergen_mapping(ingredients_list: Iterable[Tuple[List[str], List[str]]]) -> Dict[str, str]:
    lookup = defaultdict(lambda: defaultdict(int))
    for ingredients, allergens in ingredients_list:
        for ingredient, allergen in product(ingredients, allergens):
            lookup[allergen][ingredient] += 1

    def max_length_items(ingredients_count: Dict[str, int]):
        max_length = max(count for ingredient, count in ingredients_count.items())
        return tuple(ingredient for ingredient, count in ingredients_count.items() if count == max_length)

    ingredient_allergen_mapping = dict()
    while True:
        tmp = {allergen: max_length_items(ingredients) for allergen, ingredients in lookup.items()}
        try:
            allergen, ingredient = next(
                (allergen, ingredients[0]) for allergen, ingredients in tmp.items() if len(ingredients) == 1
            )
        except StopIteration:
            break
        ingredient_allergen_mapping[ingredient] = allergen

        del lookup[allergen]
        for ingredients in lookup.values():
            if ingredient in ingredients:
                del ingredients[ingredient]

    return ingredient_allergen_mapping
