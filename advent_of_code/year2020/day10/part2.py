from typing import Sequence


def count_combinations(start: int, stop: int):
    length = (stop - start) - 1
    if start == 0:
        # if this sequence starts at the very beginning, we must keep in mind
        # that we have some extra combinations that can be made
        length += 1

    # explanation:
    #  * [1, 2, 3] -> only (2,) can be removed
    #  * [1, 2, 3, 4] -> (2,), (3,) & (2, 3) can be removed
    #  * et cetera
    # This gives us the sequence (1, 3, 6, ...), which happens to be the triangular number sequence.
    # We can calculate the value for an arbitrary position as:
    #  n * (n + 1) / 2
    combinations = length * (length + 1) // 2
    return combinations + 1


def find_consecutive_ones(numbers: Sequence[int]):
    i = 0
    while i < len(numbers):
        while i < len(numbers) and numbers[i] != 1:
            i += 1
        start = i

        while i < len(numbers) and numbers[i] == 1:
            i += 1
        stop = i

        if (stop - start) > 1:
            yield start, stop


def calculate(text: str) -> int:
    joltages = sorted(map(int, text.splitlines()))

    # first make a full chain
    joltages_chain = []
    while len(joltages) > 0:
        joltages_chain.append(joltages[0])
        joltages = joltages[1:]

    # calculate the differences from the previous value
    diff_chain = tuple(b - a for a, b in zip(joltages_chain, joltages_chain[1:]))

    total = 1
    for start, stop in find_consecutive_ones(diff_chain):
        total *= count_combinations(start, stop)
    return total


puzzle = """16
10
15
5
1
11
7
19
6
12
4"""
assert calculate(puzzle) == 8

puzzle = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
assert calculate(puzzle) == 19208
