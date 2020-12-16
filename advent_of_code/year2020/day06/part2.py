from collections import defaultdict

from .shared import parse_answer_groups


def calculate(text: str) -> int:
    total_answers = 0
    for group in parse_answer_groups(text):
        answer_count = defaultdict(int)
        for person_answers in group:
            for answer in person_answers:
                answer_count[answer] += 1
        total_answers += sum(1 for count in answer_count.values() if count == len(group))
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
assert calculate(puzzle) == 6
