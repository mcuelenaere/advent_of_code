import re
from typing import NamedTuple, Union, Iterator, Iterable

RE_SPIN = re.compile(r'^s(\d+)$')
RE_EXCHANGE = re.compile(r'^x(\d+)/(\d+)$')
RE_PARTNER = re.compile(r'^p([a-z])/([a-z])$')


class Spin(NamedTuple):
    amount: int


class Exchange(NamedTuple):
    left_position: int
    right_position: int


class Partner(NamedTuple):
    left_name: str
    right_name: str


Operation = Union[Spin, Exchange, Partner]


def parse_text(text: str) -> Iterator[Operation]:
    for line in text.split(','):
        m = RE_SPIN.match(line)
        if m:
            yield Spin(amount=int(m.group(1)))
            continue

        m = RE_EXCHANGE.match(line)
        if m:
            yield Exchange(left_position=int(m.group(1)), right_position=int(m.group(2)))
            continue

        m = RE_PARTNER.match(line)
        if m:
            yield Partner(left_name=m.group(1), right_name=m.group(2))
            continue

        raise ValueError(f'Could not parse line "{line}"')


class Program(object):
    def __init__(self, programs: Iterable[str]):
        self.programs = list(programs)

    def execute_operation(self, operation: Operation):
        if isinstance(operation, Spin):
            self.programs = self.programs[-operation.amount:] + self.programs[:-operation.amount]
        elif isinstance(operation, Exchange):
            self.programs[operation.left_position], self.programs[operation.right_position] = self.programs[operation.right_position], self.programs[operation.left_position]
        elif isinstance(operation, Partner):
            left_pos, right_pos = None, None
            for i, p in enumerate(self.programs):
                if p == operation.left_name:
                    left_pos = i
                elif p == operation.right_name:
                    right_pos = i
                if left_pos is not None and right_pos is not None:
                    break

            self.programs[left_pos], self.programs[right_pos] = self.programs[right_pos], self.programs[left_pos]
        else:
            raise ValueError(f'Invalid operation {operation}')

    def __repr__(self):
        return f'Program(programs={self.programs})'

    def __str__(self):
        return ''.join(self.programs)
