from .shared import Garbage, Group, GroupOrGarbage, parse


def calculate_total_garbage_length(item: GroupOrGarbage) -> int:
    garbage_length = 0

    def _walk(item: GroupOrGarbage):
        nonlocal garbage_length
        if isinstance(item, Garbage):
            garbage_length += item.length
        elif isinstance(item, Group):
            for child in item.children:
                _walk(child)

    _walk(item)

    return garbage_length


def calculate(text: str) -> int:
    return calculate_total_garbage_length(parse(text))


GARBAGE_LENGTH = {
    "<>": 0,
    "<random characters>": 17,
    "<<<<>": 3,
    "<{!>}>": 2,
    "<!!>": 0,
    "<!!!>>": 0,
    '<{o"i!a,<{i<a>': 10,
}
for line, garbage_length in GARBAGE_LENGTH.items():
    assert calculate_total_garbage_length(parse(line)) == garbage_length
