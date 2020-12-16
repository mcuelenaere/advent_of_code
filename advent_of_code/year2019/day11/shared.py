from ..day05.shared import parse_instructions, streaming_evaluate
from collections import defaultdict
from typing import Tuple

DIRECTION_UP = 0
DIRECTION_RIGHT = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3

DIRECTION_AXIS_MAP = (
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
)


class PanelPainter(object):
    def __init__(self, text: str):
        self.instructions = parse_instructions(text)
        self.cpu = streaming_evaluate(self.instructions)
        next(self.cpu)
        self.panels = defaultdict(int)
        self.position = [0, 0]
        self.direction = DIRECTION_UP

    def _paint_panel(self, panel_color: int) -> Tuple[int, int]:
        new_color = self.cpu.send(panel_color)
        new_direction = self.cpu.send(panel_color)
        next(self.cpu)
        return new_color, new_direction

    def step(self):
        current_panel_color = self.panels[tuple(self.position)]
        new_color, turn_offset = self._paint_panel(current_panel_color)

        # paint panel new color
        self.panels[tuple(self.position)] = new_color

        if turn_offset == 0:
            # turn left
            self.direction = (self.direction - 1) % 4
        else:
            # turn right
            self.direction = (self.direction + 1) % 4

        # move into new direction
        self.position[0] += DIRECTION_AXIS_MAP[self.direction][0]
        self.position[1] += DIRECTION_AXIS_MAP[self.direction][1]

    def run(self):
        while True:
            try:
                self.step()
            except StopIteration:
                break
