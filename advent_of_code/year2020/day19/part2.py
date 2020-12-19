from .shared import RuleMatchSubRules, build_regex, parse_puzzle


def calculate(text: str) -> int:
    rules, messages = parse_puzzle(text)

    # sanity check
    assert isinstance(rules[0], RuleMatchSubRules) and rules[0].rules == (8, 11)
    assert isinstance(rules[8], RuleMatchSubRules) and rules[8].rules == (42,)
    assert isinstance(rules[11], RuleMatchSubRules) and rules[11].rules == (42, 31)

    regex_42 = build_regex(rules, 42)
    regex_31 = build_regex(rules, 31)

    # rules[0]  = 8 11
    # rules[8]  = 42 | 42 8        => 42+
    # rules[11] = 42 31 | 42 11 31 => 42 (42 (42 (42 ... 31)? 31)? 31)? 31 => 42{n} 31{n}
    def match(message: str) -> bool:
        idx = 0
        count_42 = 0
        while True:
            m = regex_42.match(message, idx)
            if m is None:
                break
            idx = m.end()
            count_42 += 1

        count_31 = 0
        while True:
            m = regex_31.match(message, idx)
            if m is None:
                break
            idx = m.end()
            count_31 += 1

        if idx != len(message):
            # must match the whole message
            return False

        if count_31 > count_42:
            # rule 11: must have at least as many 42s as there are 31s
            return False
        elif count_31 == 0:
            # rule 11: must have at least one 31
            return False
        elif count_42 - count_31 == 0:
            # rule 8: must have at least one 42
            return False

        return True

    valid_messages_count = sum(1 for message in messages if match(message))
    return valid_messages_count


puzzle = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""
assert calculate(puzzle) == 12
