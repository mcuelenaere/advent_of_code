import operator
import re
from typing import Iterable, NamedTuple, Union

RE_ASSIGN_NUMBER = re.compile(r'^(\d+) -> ([a-z]+)$')
RE_ASSIGN_WIRE = re.compile(r'^([a-z]+) -> ([a-z]+)$')
RE_BINARY_OPERATOR = re.compile(r'^(\w+) (AND|OR|LSHIFT|RSHIFT) (\w+) -> ([a-z]+)$')
RE_COMPLEMENT_OPERATOR = re.compile(r'^NOT ([a-z]+) -> ([a-z]+)$')


class AssignNumber(NamedTuple):
    value: int
    sink: str


class AssignWire(NamedTuple):
    source: str
    sink: str


class BinaryOperator(NamedTuple):
    left: Union[str, int]
    right: Union[str, int]
    operator: str
    sink: str


class ComplementOperator(NamedTuple):
    operand: str
    sink: str


Gate = Union[AssignNumber, AssignWire, BinaryOperator, ComplementOperator]


def parse_lines(lines: Iterable[str]) -> Iterable[Gate]:
    for line in lines:
        m = RE_ASSIGN_NUMBER.match(line)
        if m:
            yield AssignNumber(sink=m.group(2), value=int(m.group(1)))
            continue

        m = RE_ASSIGN_WIRE.match(line)
        if m:
            yield AssignWire(source=m.group(1), sink=m.group(2))
            continue

        m = RE_BINARY_OPERATOR.match(line)
        if m:
            yield BinaryOperator(
                left=int(m.group(1)) if m.group(1).isnumeric() else m.group(1),
                operator=m.group(2),
                right=int(m.group(3)) if m.group(3).isnumeric() else m.group(3),
                sink=m.group(4)
            )
            continue

        m = RE_COMPLEMENT_OPERATOR.match(line)
        if m:
            yield ComplementOperator(operand=m.group(1), sink=m.group(2))
            continue

        raise ValueError(f'Could not parse "{line}"')


class Circuit(object):
    BINARY_OPERATORS = {
        'AND': operator.and_,
        'OR': operator.or_,
        'LSHIFT': operator.lshift,
        'RSHIFT': operator.rshift,
    }

    def __init__(self):
        self.wires = {}
        self._wire_values = {}

    def add_gate(self, gate: Gate):
        if isinstance(gate, AssignNumber):
            self.wires[gate.sink] = lambda: gate.value
        elif isinstance(gate, AssignWire):
            self.wires[gate.sink] = lambda: self.get_wire_value(gate.source)
        elif isinstance(gate, BinaryOperator):
            self.wires[gate.sink] = lambda: self.BINARY_OPERATORS[gate.operator](
                self.get_wire_value(gate.left) if isinstance(gate.left, str) else gate.left,
                self.get_wire_value(gate.right) if isinstance(gate.right, str) else gate.right
            )
        elif isinstance(gate, ComplementOperator):
            self.wires[gate.sink] = lambda: ~self.get_wire_value(gate.operand) % 0xFFFF + 1
        else:
            raise ValueError(f"Invalid gate {gate}")

    def reset(self):
        self._wire_values = {}

    def get_wire_value(self, wire: str) -> int:
        if wire not in self._wire_values:
            self._wire_values[wire] = self.wires[wire]()
        return self._wire_values[wire]
