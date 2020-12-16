from .shared import Node, parse_tree


def sum_metadata(node: Node) -> int:
    return sum(node.metadata_entries) + sum(sum_metadata(n) for n in node.children)


def calculate(text: str) -> int:
    root = parse_tree(text)
    return sum_metadata(root)


assert calculate("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2") == 138
