from typing import Dict


class Firewall(object):
    def __init__(self, depths: Dict[int, int]):
        self.max_depths = depths
        self.timestamp = 0

    @property
    def scanner_positions(self):
        def current_position_for_depth(max_depth):
            pos = self.timestamp % (max_depth * 2 - 2)
            if pos >= max_depth:
                return max_depth - (pos - max_depth) - 2
            else:
                return pos
        return {k: current_position_for_depth(max_depth) for k, max_depth in self.max_depths.items()}

    @property
    def width(self):
        return max(k for k in self.max_depths.keys())

    @property
    def depth(self):
        return max(v for v in self.max_depths.values())

    def is_caught(self, player_position):
        return self.scanner_positions.get(player_position, -1) == 0

    def execute_step(self):
        self.timestamp += 1


def parse(text: str) -> Firewall:
    lines = (line.split(':') for line in text.splitlines())
    depths = {int(k): int(v) for k, v in lines}
    return Firewall(depths)
