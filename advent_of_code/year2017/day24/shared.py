from collections import defaultdict
from typing import Dict, Iterator, List, Set, Tuple


Component = Tuple[int, int]
Bridge = List[Component]
ComponentsByPort = Dict[int, Set[Tuple[int, Component]]]


def parse_text(text: str) -> ComponentsByPort:
    components = defaultdict(set)
    for line in text.splitlines():
        left, right = tuple(map(int, line.split("/", 2)))
        components[left].add((right, (left, right)))
        components[right].add((left, (left, right)))
    return components


def create_combinations(components: ComponentsByPort) -> Iterator[Bridge]:
    def dfs(current_pin_cnt: int, bridge: Bridge):
        for other_pin_cnt, comp in components[current_pin_cnt]:
            if comp in bridge:
                continue

            yield bridge + [comp]
            yield from dfs(other_pin_cnt, bridge + [comp])

    yield from dfs(0, [])


def calculate_bridge_strength(bridge: Bridge) -> int:
    return sum(comp[0] + comp[1] for comp in bridge)
