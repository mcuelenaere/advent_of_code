from typing import Dict, Optional, Iterable


class Firewall(object):
    def __init__(self, depths: Dict[int, int]):
        self.max_depths = depths
        self.timestamp = 0

    def get_scanner_position_at(self, x: int) -> Optional[int]:
        if x not in self.max_depths:
            return None

        max_depth = self.max_depths[x]
        pos = self.timestamp % (max_depth * 2 - 2)
        if pos >= max_depth:
            return max_depth - (pos - max_depth) - 2
        else:
            return pos

    @property
    def scanner_positions(self) -> Iterable[int]:
        return self.max_depths.keys()

    @property
    def width(self) -> int:
        return max(k for k in self.max_depths.keys())

    @property
    def depth(self) -> int:
        return max(v for v in self.max_depths.values())

    def is_caught(self, player_position: int) -> bool:
        return self.get_scanner_position_at(player_position) == 0

    def execute_step(self):
        self.timestamp += 1


def parse(text: str) -> Firewall:
    lines = (line.split(':') for line in text.splitlines())
    depths = {int(k): int(v) for k, v in lines}
    return Firewall(depths)
