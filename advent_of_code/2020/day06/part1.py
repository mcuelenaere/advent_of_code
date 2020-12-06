from .shared import parse_answer_groups
from itertools import chain


def calculate(text: str) -> int:
    total_answers = 0
    for group in parse_answer_groups(text):
        unique_answers = set(chain.from_iterable(group))
        total_answers += len(unique_answers)
    return total_answers


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
