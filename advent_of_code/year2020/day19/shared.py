import re

from typing import Dict, NamedTuple, Pattern, Tuple, Union


RuleMatchStr = NamedTuple("RuleMatchStr", text=str)
RuleMatchSubRules = NamedTuple("RuleMatchSubRules", rules=Tuple[int, ...])
RuleOneOf = NamedTuple("RuleOneOf", choices=Tuple["Rule", ...])
Rule = Union[RuleMatchStr, RuleMatchSubRules, RuleOneOf]

RE_MATCH_STR = re.compile(r"^(\d+): \"([^\"]+)\"$")
RE_MATCH_SUB_RULES = re.compile(r"^(\d+): ([\d\s\|]+)$")


def parse_puzzle(text: str):
    rules = {}
    messages = []
    mode = 1
    for line in text.splitlines():
        if line == "":
            mode = 2
            continue

        if mode == 1:
            m = RE_MATCH_STR.match(line)
            if m is not None:
                rules[int(m.group(1))] = RuleMatchStr(m.group(2))
                continue

            m = RE_MATCH_SUB_RULES.match(line)
            if m is not None:
                subgroups = m.group(2).split("|")
                subrules = tuple(
                    RuleMatchSubRules(tuple(map(int, subgroup.strip().split(" ")))) for subgroup in subgroups
                )
                rule = RuleOneOf(subrules)
                if len(rule.choices) == 1:
                    rule = rule.choices[0]
                rules[int(m.group(1))] = rule
                continue

            raise ValueError("unexpected line")
        elif mode == 2:
            messages.append(line)

    return rules, messages


def build_regex(rules: Dict[int, Rule], index: int = 0) -> Pattern[str]:
    def visit(rule: Rule):
        if isinstance(rule, RuleMatchStr):
            return re.escape(rule.text)
        elif isinstance(rule, RuleMatchSubRules):
            return "".join(visit(rules[idx]) for idx in rule.rules)
        elif isinstance(rule, RuleOneOf):
            return "(?:" + "|".join(visit(rule) for rule in rule.choices) + ")"
        else:
            raise ValueError("unknozn rule type")

    return re.compile(visit(rules[index]))
