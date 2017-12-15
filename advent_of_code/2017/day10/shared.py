from functools import reduce
from typing import Iterable, List


def reverse_part(numbers: List[int], start: int, stop: int) -> List[int]:
    for idx in range(0, (stop - start) // 2):
        # swap items
        begin_idx = (start + idx) % len(numbers)
        end_idx = (stop - 1 - idx) % len(numbers)
        numbers[begin_idx], numbers[end_idx] = numbers[end_idx], numbers[begin_idx]
    return numbers


def tie_knots(list_length: int, lengths: Iterable[int], rounds: int = 1) -> List[int]:
    index = 0
    skip_size = 0
    numbers = list(range(list_length))
    for _ in range(rounds):
        for length in lengths:
            numbers = reverse_part(numbers, index, index + length)

            index += length + skip_size
            skip_size += 1
    return numbers


def sparse_to_dense(numbers: List[int]) -> List[int]:
    def reduce_block(block: List[int]) -> int:
        return reduce(lambda a, b: a ^ b, block)

    blocks = map(reduce_block, (numbers[x*16:(x+1)*16] for x in range(16)))
    return list(blocks)
