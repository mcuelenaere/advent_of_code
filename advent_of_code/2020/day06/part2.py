from collections import defaultdict
from typing import List, Set


def parse_answers_groups(text: str) -> List[Set[str]]:
    groups = []
    current_group = defaultdict(int)
    current_group_length = 0
    for line in text.splitlines():
        if line == "":
            groups.append(set(answer for answer, count in current_group.items() if count == current_group_length))
            current_group = defaultdict(int)
            current_group_length = 0
            continue

        for answer in set(line):
            current_group[answer] += 1
        current_group_length += 1

    if len(current_group) > 0:
        groups.append(set(answer for answer, count in current_group.items() if count == current_group_length))

    return groups


def calculate(text: str) -> int:
    groups = parse_answers_groups(text)
    return sum(len(group) for group in groups)


puzzle = """abc

a
b
c

ab
ac

a
a
a
a

b"""
assert calculate(puzzle) == 6
