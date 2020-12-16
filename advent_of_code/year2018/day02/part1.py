from collections import defaultdict
from typing import Tuple, Dict


def freq_count(items: Tuple[str]) -> Dict[str, int]:
    counts = defaultdict(lambda: 0)
    for item in items:
        counts[item] += 1
    return counts


def calculate(text: str) -> int:
    boxes_with_two = 0
    boxes_with_three = 0

    for id in text.splitlines():
        has_two = False
        has_three = False
        for letter, occurences in freq_count(tuple(id)).items():
            if occurences == 2:
                has_two = True
            elif occurences == 3:
                has_three = True

        if has_two:
            boxes_with_two += 1
        if has_three:
            boxes_with_three += 1

    return boxes_with_two * boxes_with_three


puzzle = """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
""".strip()
assert calculate(puzzle) == 12
