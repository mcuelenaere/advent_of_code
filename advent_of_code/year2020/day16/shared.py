import re

from typing import List, NamedTuple, Tuple


RE_RULE = re.compile(r"^([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)$")

Ticket = Tuple[int, ...]


class Bounds(NamedTuple):
    min: int
    max: int


class Rule(NamedTuple):
    name: str
    bounds: Tuple[Bounds, Bounds]


def parse_data(text: str) -> Tuple[List[Rule], Ticket, List[Ticket]]:
    rules = []
    your_ticket = None
    nearby_tickets = []
    part = 1
    for line in text.splitlines():
        if line == "your ticket:":
            part = 2
            continue
        elif line == "nearby tickets:":
            part = 3
            continue
        elif line == "":
            continue

        if part == 1:
            m = RE_RULE.match(line)
            assert m is not None
            rules.append(
                Rule(
                    name=m.group(1),
                    bounds=(
                        Bounds(int(m.group(2)), int(m.group(3))),
                        Bounds(int(m.group(4)), int(m.group(5))),
                    ),
                )
            )
        elif part == 2:
            your_ticket = tuple(map(int, line.split(",")))
        elif part == 3:
            nearby_tickets.append(tuple(map(int, line.split(","))))
    return rules, your_ticket, nearby_tickets
