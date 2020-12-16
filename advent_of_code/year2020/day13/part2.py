from functools import reduce
from typing import Iterable, Tuple

from .shared import parse_schedule


def mult(iterable: Iterable[int]) -> int:
    return reduce(lambda a, b: a * b, iterable)


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


# adapted from https://stackoverflow.com/a/9758173
def modinv(a: int, m: int) -> int:
    g, x, y = egcd(a, m)
    if g != 1:
        raise RuntimeError("modular inverse does not exist")
    else:
        return x % m


def calculate(text: str) -> int:
    _, bus_lines = parse_schedule(text)
    lines = tuple(filter(lambda x: x[1] is not None, enumerate(bus_lines)))

    # given:
    #  line= 7, delay=0
    #  line=13, delay=1
    #  line=59, delay=4
    #  line=31, delay=6
    #  line=19, delay=7
    # we come up with the following list of equations:
    #  x % 7 = 0        <=> x = 0 mod 7
    #  x % 13 = 13 - 1  <=> x = 12 mod 13
    #  x % 59 = 59 - 4  <=> x = 55 mod 59
    #  x % 31 = 31 - 6  <=> x = 25 mod 31
    #  x % 19 = 19 - 7  <=> x = 12 mod 19
    #
    # We solve this using Chinese Remainder Theorem (https://math.stackexchange.com/a/1108148):
    #  x = sum(a(n) * M(n) * M'(n)) % mult(m)
    a = tuple(line - delay for delay, line in lines)
    m = tuple(line for delay, line in lines)
    M = lambda i: mult(m) // m[i]
    return sum(a[i] * M(i) * modinv(M(i), m[i]) for i in range(len(a))) % mult(m)


puzzle = """0
7,13,x,x,59,x,31,19"""
assert calculate(puzzle) == 1068781
puzzle = """0
17,x,13,19"""
assert calculate(puzzle) == 3417
puzzle = """0
67,7,59,61"""
assert calculate(puzzle) == 754018
puzzle = """0
67,x,7,59,61"""
assert calculate(puzzle) == 779210
puzzle = """0
67,7,x,59,61"""
assert calculate(puzzle) == 1261476
puzzle = """0
1789,37,47,1889"""
assert calculate(puzzle) == 1202161486
