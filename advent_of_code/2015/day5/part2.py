import re

RE_NICE = (
    re.compile(r'^.*([a-z])([a-z])(?!\2).*\1\2.*$'),
    re.compile(r'^.*([a-z])[a-z]\1.*$'),
)


def is_nice(line: str) -> bool:
    return all(regex.match(line) for regex in RE_NICE)


def calculate(text: str) -> int:
    return sum(1 if is_nice(line) else 0 for line in text.splitlines())


assert calculate("qjhvhtzxzqqjkmpb") == 1
assert calculate("xxyxx") == 1
assert calculate("uurcxstgmygtbstg") == 0
assert calculate("ieodomkazucvgmuy") == 0
