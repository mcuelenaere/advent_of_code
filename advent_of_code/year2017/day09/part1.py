from .shared import Garbage, Group, GroupOrGarbage, parse


def calculate_score(item: GroupOrGarbage) -> int:
    def _calc(item: GroupOrGarbage, depth: int) -> int:
        if isinstance(item, Garbage):
            return 0
        elif isinstance(item, Group):
            return depth + sum(_calc(child, depth + 1) for child in item.children)

    return _calc(item, 1)


def calculate(text: str) -> int:
    return calculate_score(parse(text))


GROUPS_SCORE = {
    "{}": 1,
    "{{{}}}": 6,
    "{{},{}}": 5,
    "{{{},{},{{}}}}": 16,
    "{<a>,<a>,<a>,<a>}": 1,
    "{{<ab>},{<ab>},{<ab>},{<ab>}}": 9,
    "{{<!!>},{<!!>},{<!!>},{<!!>}}": 9,
    "{{<a!>},{<a!>},{<a!>},{<ab>}}": 3,
}
for line, score in GROUPS_SCORE.items():
    assert calculate(line) == score
