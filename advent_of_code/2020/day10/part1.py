from collections import defaultdict


def calculate(text: str) -> int:
    joltages = sorted(map(int, text.splitlines()))

    current_joltage = 0
    differences = defaultdict(int)
    while len(joltages) > 0:
        new_joltage = joltages[0]
        joltages = joltages[1:]
        differences[new_joltage - current_joltage] += 1
        current_joltage = new_joltage
    differences[3] += 1

    return differences[1] * differences[3]


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
assert calculate(puzzle) == 7 * 5

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
assert calculate(puzzle) == 22 * 10
