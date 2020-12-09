from typing import Sequence


def find_first_non_sum(numbers: Sequence[int], preamble_length: int = 25) -> int:
    for i in range(preamble_length, len(numbers)):
        valid_numbers = set()
        for j in range(i - preamble_length, i):
            for k in range(j + 1, i):
                valid_numbers.add(numbers[j] + numbers[k])
        if numbers[i] not in valid_numbers:
            return numbers[i]
