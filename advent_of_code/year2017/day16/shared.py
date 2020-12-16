import re
from typing import NamedTuple, Union, Iterator, Iterable

RE_SPIN = re.compile(r'^s(\d+)$')
RE_EXCHANGE = re.compile(r'^x(\d+)/(\d+)$')
RE_PARTNER = re.compile(r'^p([a-z])/([a-z])$')


Spin = NamedTuple('Spin', amount=int)
Exchange = NamedTuple('Exchange', left_position=int, right_position=int)
Partner = NamedTuple('Partner', left_name=str, right_name=str)
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

    def _swap(self, x, y):
        self.programs[x], self.programs[y] = self.programs[y], self.programs[x]

    def execute_operation(self, operation: Operation):
        if isinstance(operation, Spin):
            self.programs = self.programs[-operation.amount:] + self.programs[:-operation.amount]
        elif isinstance(operation, Exchange):
            self._swap(operation.left_position, operation.right_position)
        elif isinstance(operation, Partner):
            self._swap(
                self.programs.index(operation.left_name),
                self.programs.index(operation.right_name)
            )
        else:
            raise ValueError(f'Invalid operation {operation}')

    def __repr__(self):
        return f'Program(programs={self.programs})'

    def __str__(self):
        return ''.join(self.programs)
