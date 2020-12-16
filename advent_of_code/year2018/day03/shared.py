import re

from collections import defaultdict
from typing import Dict, Iterable, NamedTuple, Set, Tuple


class Claim(NamedTuple):
    id: int
    left: int
    top: int
    width: int
    height: int

    @property
    def covered_coordinates(self) -> Iterable[Tuple[int, int]]:
        for x in range(self.left, self.left + self.width):
            for y in range(self.top, self.top + self.height):
                yield (x, y)


RE_CLAIM = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


def parse_claims(lines: str) -> Iterable[Claim]:
    for line in lines.splitlines():
        m = RE_CLAIM.match(line)
        if m:
            yield Claim(
                id=int(m.group(1)),
                left=int(m.group(2)),
                top=int(m.group(3)),
                width=int(m.group(4)),
                height=int(m.group(5)),
            )


def build_fabric(claims: Iterable[Claim]) -> Dict[Tuple[int, int], Set[int]]:
    fabric = defaultdict(lambda: set())
    for claim in claims:
        for x, y in claim.covered_coordinates:
            fabric[(x, y)].add(claim.id)
    return fabric
