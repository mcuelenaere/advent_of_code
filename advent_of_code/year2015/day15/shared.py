from collections import Counter
from functools import reduce
from typing import Dict, Iterable, Iterator, Tuple


def parse_text(text: str) -> Iterator[Tuple[str, Dict[str, int]]]:
    for line in text.splitlines():
        name, properties = line.split(": ")
        properties = {p.split(" ")[0]: int(p.split(" ")[1]) for p in properties.split(", ")}
        yield name, properties


def calculate_score(properties: Iterable[Dict[str, int]], weights: Iterable[int]) -> int:
    totals = Counter()
    for props, weight in zip(properties, weights):
        totals.update({k: v * weight for k, v in props.items()})

    if any(v < 0 for v in totals.values()):
        return 0

    return reduce(lambda a, b: a * b, totals.values(), 1)
