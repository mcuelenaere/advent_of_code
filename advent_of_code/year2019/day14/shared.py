from collections import defaultdict
from itertools import groupby
from math import ceil
from typing import NamedTuple, Tuple, Iterable


class Quantity(NamedTuple):
    chemical: str
    units: int

    def __sub__(self, other) -> 'Quantity':
        if not isinstance(other, int):
            raise TypeError()
        return Quantity(self.chemical, self.units - other)

    def __mul__(self, other) -> 'Quantity':
        if not isinstance(other, int):
            raise TypeError()
        return Quantity(self.chemical, self.units * other)


class Reaction(NamedTuple):
    inputs: Tuple[Quantity]
    output: Quantity

    def __mul__(self, other) -> 'Reaction':
        if not isinstance(other, int):
            raise TypeError()
        return Reaction(tuple(input * other for input in self.inputs), self.output * other)


def parse_quantity(text: str) -> Quantity:
    units, chemical = text.split(' ', 2)
    return Quantity(chemical=chemical, units=int(units))


def parse_reactions(text: str) -> Iterable[Reaction]:
    for line in text.splitlines():
        inputs, output = line.split(' => ')
        inputs = inputs.split(', ')
        yield Reaction(
            inputs=tuple(map(parse_quantity, inputs)),
            output=parse_quantity(output)
        )


def minimum_ore(reactions: Tuple[Reaction], quantity: Quantity):
    reactions_by_output = dict((k, tuple(v)) for k, v in groupby(reactions, key=lambda r: r.output.chemical))
    waste = defaultdict(int)

    def find(requested: Quantity) -> int:
        if requested.chemical == 'ORE':
            return requested.units

        # check if there's waste available
        if waste[requested.chemical] > 0:
            reuse = min(requested.units, waste[requested.chemical])
            requested -= reuse
            waste[requested.chemical] -= reuse

        assert len(reactions_by_output[requested.chemical]) == 1
        reaction = reactions_by_output[requested.chemical][0]

        # calculate total ore required
        multiplier = ceil(requested.units / reaction.output.units)
        total_ore = sum(find(input * multiplier) for input in reaction.inputs)

        # keep track of waste
        waste[requested.chemical] += multiplier * reaction.output.units - requested.units

        return total_ore

    return find(quantity)
