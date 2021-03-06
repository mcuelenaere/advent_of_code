from .shared import (
    ACRE_LUMBERYARD,
    ACRE_TREE,
    advance_lumber_area,
    freq_count,
    parse_lumber_area,
)


def calculate(text: str) -> int:
    lumber_area = parse_lumber_area(text)
    for _ in range(10):
        lumber_area = advance_lumber_area(lumber_area)
    acre_count = freq_count(lumber_area.values())
    return acre_count[ACRE_TREE] * acre_count[ACRE_LUMBERYARD]


puzzle = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".strip()
assert calculate(puzzle) == 1147
