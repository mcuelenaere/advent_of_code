import re
from typing import Iterable, NamedTuple, Tuple

RE_LIGHT = re.compile(r'^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)$')
MAX_SIZE = 1000


class Line(NamedTuple):
    action: str
    start: Tuple[int, int]
    stop: Tuple[int, int]


def parse_lines(lines: Iterable[str]) -> Iterable[Line]:
    for line in lines:
        m = RE_LIGHT.match(line)
        if m is None:
            raise ValueError(f"Invalid line {line}")
        yield Line(
            action=m.group(1),
            start=(int(m.group(2)), int(m.group(3))),
            stop=(int(m.group(4)), int(m.group(5))),
        )


def execute_light_configuration(lines: Iterable[Line], default_val, action_parser: callable):
    configuration = list([default_val] * MAX_SIZE for _ in range(MAX_SIZE))
    for line in lines:
        op = action_parser(line.action)
        for x in range(line.start[0], line.stop[0] + 1):
            for y in range(line.start[1], line.stop[1] + 1):
                configuration[x][y] = op(configuration[x][y])
    return configuration
