from functools import reduce
from typing import Iterable


def parse_packages(text: str) -> Iterable[int]:
    return (int(line) for line in text.splitlines())


def quantum_entanglement(packages: Iterable[int]) -> int:
    return reduce(lambda a, b: a * b, packages)
