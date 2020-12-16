from typing import Tuple, Dict, Iterable, List

Replacements = Dict[str, List[str]]


def parse_input(text: str) -> Tuple[Replacements, str]:
    lines = text.splitlines()

    # last line is formula
    formula = lines.pop()

    # remove empty line
    assert lines.pop() == ""

    # parse replacements
    replacements = {}
    for line in lines:
        key, val = line.split(' => ')
        if key not in replacements:
            replacements[key] = []
        replacements[key].append(val)

    return replacements, formula


def generate_possibilities(formula: str, replacements: Replacements) -> Iterable[str]:
    for search, values in replacements.items():
        i = -1
        while i < len(formula):
            i = formula.find(search, i + 1)
            if i == -1:
                break
            for x in values:
                yield formula[:i] + x + formula[i + len(search):]


def create_inverse_map(replacements: Replacements) -> Dict[str, str]:
    out = {}
    for key, values in replacements.items():
        for value in values:
            assert value not in out
            out[value] = key
    return out


def find_fewest_steps(formula: str, replacements: Replacements) -> int:
    inverse_map = create_inverse_map(replacements)  # a suffix tree would be much better actually
    longest_key = max(len(x) for x in inverse_map.keys())

    steps = 0
    while formula != 'e':
        found = False
        index = len(formula)
        while index > 0:
            # find longest matching suffix
            for i in range(longest_key, 0, -1):
                replacement = inverse_map.get(formula[index-i:index], None)
                if replacement == 'e' and index != i:
                    # we cannot replace with the goal yet if this isn't the last replacement
                    continue

                if replacement:
                    formula = formula[:index-i] + replacement + formula[index:]
                    found = True
                    break

            if found:
                break
            else:
                # no substitution found, try looking further ahead
                index -= 1

        if not found:
            raise RuntimeError('Suffix not found!')
        steps += 1
    return steps
