from .shared import Node, parse_tree


def calculate_node_value(node: Node) -> int:
    if len(node.children) == 0:
        return sum(node.metadata_entries)
    else:
        value = 0
        for index in node.metadata_entries:
            index -= 1  # indexes are 0-based

            if index >= len(node.children) or index < 0:
                # child does not exist
                continue

            value += calculate_node_value(node.children[index])
        return value


def calculate(text: str) -> int:
    root = parse_tree(text)
    return calculate_node_value(root)


assert calculate("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2") == 66
