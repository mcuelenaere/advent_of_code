from collections import defaultdict


def calculate(text: str) -> int:
    min_number_of_presents = int(text)

    present_counts = defaultdict(lambda: 0)
    for elf in range(1, min_number_of_presents // 10 + 1):
        for house in range(elf, min_number_of_presents // 10 + 1, elf):
            present_counts[house] += elf * 10

    for k, v in present_counts.items():
        if v >= min_number_of_presents:
            return k


assert calculate("10") == 1
assert calculate("30") == 2
assert calculate("40") == 3
assert calculate("70") == 4
assert calculate("120") == 6
assert calculate("150") == 8
