from functools import reduce
from typing import Iterable, Tuple

from ..day10.shared import sparse_to_dense, tie_knots


def reduce_to_big_number(numbers: Iterable[int]) -> int:
    return reduce(lambda prev, cur: (prev << 8) | cur, numbers, 0)


def calculate_rows(text: str) -> Iterable[int]:
    for i in range(128):
        lengths = list(map(lambda x: ord(x), f"{text}-{i}"))
        lengths.extend([17, 31, 73, 47, 23])
        sparse = tie_knots(256, lengths, rounds=64)
        dense = sparse_to_dense(sparse)
        big = reduce_to_big_number(dense)
        yield big


def walk_as_grid(numbers: Iterable[int]) -> Iterable[Tuple[int, int, bool]]:
    for x, row in enumerate(numbers):
        binary_str = bin(row).replace("0b", "").zfill(128)
        for y, bit in enumerate(binary_str):
            yield (x, y, bit == "1")
