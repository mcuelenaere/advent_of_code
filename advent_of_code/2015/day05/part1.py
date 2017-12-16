import re

RE_NICE = (
    re.compile(r'^(.*[aeiou].*){3,}$'),
    re.compile(r'^.*([a-z])\1.*$'),
    re.compile(r'^((?!ab|cd|pq|xy).)*$'),
)


def is_nice(line: str) -> bool:
    return all(regex.match(line) for regex in RE_NICE)


def calculate(text: str) -> int:
    return sum(1 if is_nice(line) else 0 for line in text.splitlines())


assert calculate("ugknbfddgicrmopn") == 1
assert calculate("aaa") == 1
assert calculate("jchzalrnumimnmhp") == 0
assert calculate("haegwjzuvuyypxyu") == 0
assert calculate("dvszwmarrgswjxmb") == 0
