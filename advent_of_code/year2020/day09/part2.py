from typing import Optional, Sequence

from .shared import find_first_non_sum


def find_contiguous_sum(numbers: Sequence[int], search_value: int) -> Optional[Sequence[int]]:
    for contiguous_length in range(2, len(numbers)):
        rolling_sum = 0
        for i in range(contiguous_length):
            rolling_sum += numbers[i]

        for i in range(len(numbers) - contiguous_length):
            if search_value == rolling_sum:
                return numbers[i : i + contiguous_length]

            rolling_sum -= numbers[i]
            rolling_sum += numbers[i + contiguous_length]

    return None


def calculate(text: str, preamble_length: int = 25) -> int:
    numbers = tuple(map(int, text.splitlines()))
    invalid_number = find_first_non_sum(numbers, preamble_length)
    subset = find_contiguous_sum(numbers, invalid_number)
    assert subset is not None
    return min(subset) + max(subset)


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
assert calculate(puzzle, 5) == 62
