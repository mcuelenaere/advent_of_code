import re

from typing import Dict, List, Tuple


RE_BAG_LINE = re.compile(r"^([\w\s]+) bags contain (.+)\.$")
RE_BAG_PART = re.compile(r"(\d+) ([\w\s]+) bags?(?:, )?")


def parse_rules(text: str) -> Dict[str, List[Tuple[str, int]]]:
    tree = {}
    for line in text.splitlines():
        m = RE_BAG_LINE.match(line)
        assert m is not None
        parent_type = m.group(1)
        children = []
        for amount, bag_type in RE_BAG_PART.findall(m.group(2)):
            children.append((bag_type, int(amount)))
        tree[parent_type] = children
    return tree
