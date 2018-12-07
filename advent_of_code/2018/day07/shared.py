import re
from typing import Iterable, Tuple, NamedTuple, Set


RE_REQUIREMENT = re.compile(r'^Step (\w) must be finished before step (\w) can begin\.$')


def parse_requirements(text: str) -> Iterable[Tuple[str, str]]:
    for line in text.splitlines():
        m = RE_REQUIREMENT.match(line)
        if m:
            yield m.group(1), m.group(2)


class TreeNode(NamedTuple):
    name: str
    children: Set[str]
    parents: Set[str]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return type(other) == type(self) and other.name == self.name


class Tree(dict):
    def __missing__(self, key):
        self[key] = TreeNode(name=key, children=set(), parents=set())
        return self[key]

    @property
    def roots(self) -> Set[TreeNode]:
        dependents = set()
        for node in self.values():
            dependents.update(node.children)
        root_labels = self.keys() - dependents
        return {self[l] for l in root_labels}


def build_tree(text: str) -> Tree:
    tree = Tree()
    for step_prev, step_next in parse_requirements(text):
        tree[step_prev].children.add(step_next)
        tree[step_next].parents.add(step_prev)
    return tree
