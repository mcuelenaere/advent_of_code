import re
from typing import Iterator, Tuple, Dict

RE_LINE = re.compile(r'^Sue (\d+): (.+)$')


def parse_text(text: str) -> Iterator[Tuple[str, Dict[str, int]]]:
    for line in text.splitlines():
        m = RE_LINE.match(line)
        if not m:
            raise ValueError(f'Invalid line "{line}"')

        sue_number, props = m.groups()
        props = {p.split(': ')[0]: int(p.split(': ')[1]) for p in props.split(', ')}
        yield int(sue_number), props
