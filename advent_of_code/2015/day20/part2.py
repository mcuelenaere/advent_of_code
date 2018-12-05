from collections import defaultdict


def calculate(text: str) -> int:
    min_number_of_presents = int(text)

    present_counts = defaultdict(lambda: 0)
    for elf in range(1, min_number_of_presents // 11 + 1):
        for delivered_count, house in enumerate(range(elf, min_number_of_presents // 11 + 1, elf)):
            if delivered_count >= 50:
                break
            present_counts[house] += elf * 11

    for k, v in present_counts.items():
        if v >= min_number_of_presents:
            return k
