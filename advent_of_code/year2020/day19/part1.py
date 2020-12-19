from .shared import build_regex, parse_puzzle


def calculate(text: str) -> int:
    rules, messages = parse_puzzle(text)
    regex = build_regex(rules)
    valid_messages_count = 0
    for message in messages:
        m = regex.match(message)
        if m is not None and m.end() == len(message):
            valid_messages_count += 1
    return valid_messages_count


puzzle = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
assert calculate(puzzle) == 2
