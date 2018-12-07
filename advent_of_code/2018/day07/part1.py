from .shared import build_tree, Tree, TreeNode
from typing import Iterable


def walk_tree(tree: Tree) -> Iterable[TreeNode]:
    queue = tree.roots
    already_seen = set()
    while len(queue) > 0:
        # pick next node
        node = next(n for n in sorted(queue, key=lambda n: n.name) if already_seen.issuperset(n.parents))

        # process it
        queue.remove(node)
        yield node
        already_seen.add(node.name)

        # add its children to the queue
        for child_label in sorted(node.children):
            queue.add(tree[child_label])


def calculate(text: str) -> str:
    tree = build_tree(text)
    return ''.join(node.name for node in walk_tree(tree))


puzzle = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip()
assert calculate(puzzle) == "CABDFE"
