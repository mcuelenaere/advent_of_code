from .shared import parse_text


def calculate(text: str) -> int:
    gen_a, gen_b = parse_text(text)
    counter = 0
    for _ in range(40_000_000):
        val_a, val_b = next(gen_a), next(gen_b)
        val_a &= 0xFFFF
        val_b &= 0xFFFF
        if val_a == val_b:
            counter += 1
    return counter


puzzle = """
Generator A starts with 65
Generator B starts with 8921
""".strip()
gen_a, gen_b = parse_text(puzzle)
assert next(gen_a) == 1092455
assert next(gen_a) == 1181022009
assert next(gen_a) == 245556042
assert next(gen_a) == 1744312007
assert next(gen_a) == 1352636452
assert next(gen_b) == 430625591
assert next(gen_b) == 1233683848
assert next(gen_b) == 1431495498
assert next(gen_b) == 137874439
assert next(gen_b) == 285222916
assert calculate(puzzle) == 588
