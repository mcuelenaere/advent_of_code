from collections import defaultdict
from typing import Iterable, Tuple, List


def sorted_freq_count(letters: Iterable[str]) -> Tuple[str, ...]:
    freq_count = defaultdict(lambda: 0)
    for letter in letters:
        freq_count[letter] += 1
    return tuple(letter for letter, cnt in sorted(freq_count.items(), key=lambda x: x[1], reverse=True))


def parse_columns(text: str) -> Tuple[List[str], ...]:
    lines = text.splitlines()
    columns = tuple([] for _ in range(len(lines[0])))
    for line in lines:
        for i in range(len(columns)):
            columns[i].append(line[i])
    return columns
