import re

from typing import Tuple


RE_PASSWORD_LINE = re.compile(r"^(\d+)-(\d+) (\w): (\w+)$")


def parse_password_line(line: str) -> Tuple[int, int, str, str]:
    m = RE_PASSWORD_LINE.match(line)
    assert m is not None

    return int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
