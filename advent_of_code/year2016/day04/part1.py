from .shared import is_real_room, parse_instructions


def calculate(text: str) -> int:
    return sum(instruction.sector_id for instruction in parse_instructions(text) if is_real_room(instruction))


puzzle = """
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
""".strip()
assert calculate(puzzle) == 1514
