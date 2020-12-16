from .shared import build_fabric, parse_claims


def calculate(text: str) -> int:
    fabric = build_fabric(parse_claims(text))

    non_overlapping_ids = set()
    overlapping_ids = set()
    for ids in fabric.values():
        if len(ids) == 1:
            non_overlapping_ids.update(ids)
        else:
            overlapping_ids.update(ids)

    result = tuple(non_overlapping_ids - overlapping_ids)
    assert len(result) == 1
    return result[0]


puzzle = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
""".strip()
assert calculate(puzzle) == 3
