from .shared import parse_rules


def calculate(text: str):
    rules = parse_rules(text)

    # recursively count all child bags for a given bag type
    def dfs(bag_type: str):
        total_count = 1
        for child_bag_type, count in rules[bag_type]:
            total_count += count * dfs(child_bag_type)
        return total_count

    return dfs("shiny gold") - 1


puzzle = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
assert calculate(puzzle) == 32

puzzle = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""
assert calculate(puzzle) == 126
