import re

from typing import Iterable, NamedTuple, Tuple


IP = NamedTuple("IP", supernet_sequences=Tuple[str, ...], hypernet_sequences=Tuple[str, ...])
RE_HYPERNET = re.compile(r"\[[a-z]+\]")
RE_ABBA = re.compile(r"([a-z])([a-z])\2\1")


def parse_ips(text: str) -> Iterable[IP]:
    for line in text.splitlines():
        supernets = tuple(RE_HYPERNET.split(line))
        hypernets = tuple(m[1:-1] for m in RE_HYPERNET.findall(line))
        yield IP(supernet_sequences=supernets, hypernet_sequences=hypernets)


def find_abbas(text: str) -> Tuple[str, ...]:
    return tuple(m.group(0) for m in RE_ABBA.finditer(text) if m.group(1) != m.group(2))


def find_abas(text: str) -> Tuple[str, ...]:
    # regexes can't be used, as those are non-overlapping
    return tuple(a + b + c for a, b, c in zip(text, text[1:], text[2:]) if a != b and a == c)
