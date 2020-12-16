from typing import Iterator


def parse_text(text: str) -> Iterator[int]:
    return map(int, text.splitlines())
