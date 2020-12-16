import re
from typing import Tuple, Iterator

RE_GENERATOR_LINE = re.compile(r'^Generator (\w+) starts with (\d+)$')
GENERATOR_MULTIPLIERS = {
    'A': 16807,
    'B': 48271,
}
GENERATOR_MULTIPLES = {
    'A': 4,
    'B': 8,
}


def parse_text(text: str, check_multiples: bool = False) -> Tuple[Iterator[int], Iterator[int]]:
    start_values = {}
    for line in text.splitlines():
        m = RE_GENERATOR_LINE.match(line)
        if m is None:
            raise ValueError()
        start_values[m.group(1)] = int(m.group(2))

    assert set(start_values.keys()) == {'A', 'B'}, "Text did not contain both generators A and B"

    def create_generator(type: str) -> Iterator[int]:
        value = start_values[type]
        multiplier = GENERATOR_MULTIPLIERS[type]
        if check_multiples:
            multiple = GENERATOR_MULTIPLES[type]
            while True:
                value *= multiplier
                value %= 2147483647
                if value % multiple == 0:
                    yield value
        else:
            while True:
                value *= multiplier
                value %= 2147483647
                yield value

    return (
        create_generator('A'),
        create_generator('B'),
    )
