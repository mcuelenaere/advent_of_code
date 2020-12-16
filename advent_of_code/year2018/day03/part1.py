from .shared import build_fabric, parse_claims


def calculate(text: str) -> int:
    fabric = build_fabric(parse_claims(text))
    return sum(1 for ids in fabric.values() if len(ids) >= 2)


puzzle = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
""".strip()
assert calculate(puzzle) == 4
