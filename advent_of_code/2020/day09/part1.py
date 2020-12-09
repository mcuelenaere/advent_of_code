from .shared import find_first_non_sum


def calculate(text: str, preamble_length: int = 25) -> int:
    numbers = tuple(map(int, text.splitlines()))
    return find_first_non_sum(numbers, preamble_length)


puzzle = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
assert calculate(puzzle, 5) == 127
