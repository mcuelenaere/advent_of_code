from collections import defaultdict

from .shared import find_root, parse_lines


def build_weight_map(lines):
    return {name: (weight, children) for name, weight, children in lines}


def calculate_total_weight(node_name, weight_map):
    node_weight, children = weight_map[node_name]
    return node_weight + sum(calculate_total_weight(child, weight_map) for child in children)


def find_standard_and_outlier(items):
    freq_count = defaultdict(int)
    for v in items:
        freq_count[v] += 1
    outlier = next((k for k, v in freq_count.items() if v == 1), None)
    standard = next(k for k, v in freq_count.items() if v != 1)
    return standard, outlier


def find_weight_diff(root, weight_map):
    child_weights = {child: calculate_total_weight(child, weight_map) for child in weight_map[root][1]}
    standard, outlier = find_standard_and_outlier(child_weights.values())
    outlier_child = next((child for child, weight in child_weights.items() if weight == outlier), None)
    return outlier_child, standard, outlier


def calculate(text: str) -> int:
    lines = text.splitlines()
    lines = tuple(parse_lines(lines))
    root = find_root(lines)
    weight_map = build_weight_map(lines)

    cur = root
    cur_diff = 0
    while True:
        outlier_child, standard, outlier = find_weight_diff(cur, weight_map)
        if outlier_child is None:
            return weight_map[cur][0] - cur_diff
        else:
            cur = outlier_child
            cur_diff = outlier - standard


puzzle = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
""".strip()

assert calculate(puzzle) == 60
