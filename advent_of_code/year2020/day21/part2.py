from .shared import build_ingredient_allergen_mapping, parse_ingredients


def calculate(text: str) -> str:
    mapping = build_ingredient_allergen_mapping(parse_ingredients(text))
    return ",".join(k for k, v in sorted(mapping.items(), key=lambda x: x[1]))


puzzle = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
assert calculate(puzzle) == "mxmxvkd,sqjhc,fvjkl"
