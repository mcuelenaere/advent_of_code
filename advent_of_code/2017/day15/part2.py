from .shared import parse_text


def calculate(text: str) -> int:
    gen_a, gen_b = parse_text(text, check_multiples=True)
    counter = 0
    for _ in range(5_000_000):
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
gen_a, gen_b = parse_text(puzzle, check_multiples=True)
assert next(gen_a) == 1352636452
assert next(gen_a) == 1992081072
assert next(gen_a) == 530830436
assert next(gen_a) == 1980017072
assert next(gen_a) == 740335192
assert next(gen_b) == 1233683848
assert next(gen_b) == 862516352
assert next(gen_b) == 1159784568
assert next(gen_b) == 1616057672
assert next(gen_b) == 412269392
assert calculate(puzzle) == 309
