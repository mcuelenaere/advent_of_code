import re
from itertools import permutations
from typing import Dict, Tuple

RE_LINE = re.compile(r'^(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).$')
Configuration = Dict[Tuple[str, str], int]


def parse_text(text: str) -> Configuration:
    configuration = {}
    for line in text.splitlines():
        m = RE_LINE.match(line)
        if not m:
            raise ValueError(f'Could not parse line "{line}"')
        left, gain_lose, amount, right = m.groups()
        sign = 1 if gain_lose == 'gain' else -1
        configuration[(left, right)] = sign * int(amount)
    return configuration


def calculate_happiness(config: Configuration, combination: Tuple[str]) -> int:
    combination = combination[:] + combination[:1]
    return sum(config[(a, b)] + config[(b, a)] for a, b in zip(combination, combination[1:]))


def find_maximum_happiness(config: Configuration) -> int:
    unique_names = {x[0] for x in config.keys()}
    return max(calculate_happiness(config, permutation) for permutation in permutations(unique_names, len(unique_names)))
