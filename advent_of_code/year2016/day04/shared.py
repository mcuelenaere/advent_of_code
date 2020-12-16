import re

from collections import defaultdict
from typing import Iterable, NamedTuple


Instruction = NamedTuple("Instruction", encrypted_name=str, sector_id=int, checksum=str)
RE_INSTRUCTION = re.compile(r"^([a-z-\-]+)-(\d+)\[([a-z\-]+)\]$")


def parse_instructions(text: str) -> Iterable[Instruction]:
    for line in text.splitlines():
        m = RE_INSTRUCTION.match(line)
        if m:
            yield Instruction(
                encrypted_name=m.group(1),
                sector_id=int(m.group(2)),
                checksum=m.group(3),
            )


def is_real_room(instruction: Instruction) -> bool:
    freq_count = defaultdict(lambda: 0)
    for letter in instruction.encrypted_name:
        if letter == "-":
            continue
        freq_count[letter] += 1

    most_common_letters = [letter for letter, count in sorted(freq_count.items(), key=lambda x: (-x[1], x[0]))][:5]
    return instruction.checksum == "".join(most_common_letters)
