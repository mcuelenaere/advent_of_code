import re
from typing import NamedTuple, Tuple, Union, Iterable

RE_BITMASK = re.compile(r"^mask = ([X\d]+)$")
RE_MEM = re.compile(r"^mem\[(\d+)\] = (\d+)$")


class Bitmask(NamedTuple):
    bits: Tuple[Tuple[int, str], ...]


class MemoryWrite(NamedTuple):
    address: int
    data: int


def parse_operations(text: str) -> Iterable[Union[Bitmask, MemoryWrite]]:
    for line in text.splitlines():
        m = RE_BITMASK.match(line)
        if m is not None:
            bits = tuple(enumerate(reversed(m.group(1))))
            yield Bitmask(bits)
            continue

        m = RE_MEM.match(line)
        if m is not None:
            address = int(m.group(1))
            data = int(m.group(2))
            yield MemoryWrite(address, data)
            continue
