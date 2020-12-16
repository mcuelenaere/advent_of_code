from collections import defaultdict, deque

from .shared import parse_rules


def calculate(text: str):
    rules = parse_rules(text)

    # build inverted dependency tree
    inv_dep_tree = defaultdict(set)
    for parent, children in rules.items():
        for child, _ in children:
            inv_dep_tree[child].add(parent)

    # build set of all possible parents for "shiny gold"
    parents = set()
    stack = deque(["shiny gold"])
    while len(stack) > 0:
        bag_type = stack.pop()
        for child in inv_dep_tree[bag_type]:
            stack.append(child)
            parents.add(child)

    return len(parents)


puzzle = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
assert calculate(puzzle) == 4
