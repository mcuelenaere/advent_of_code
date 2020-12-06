from typing import List, Set


def parse_answers_groups(text: str) -> List[Set[str]]:
    groups = []
    current_group = set()
    for line in text.splitlines():
        if line == "":
            groups.append(current_group)
            current_group = set()
            continue

        answers = set(line)
        current_group.update(answers)

    if len(current_group) > 0:
        groups.append(current_group)

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
assert calculate(puzzle) == 11
