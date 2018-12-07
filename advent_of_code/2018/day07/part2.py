from .shared import build_tree, TreeNode
from typing import Optional


class Worker(object):
    def __init__(self, step_overhead: int):
        self.step_overhead = step_overhead
        self.blocked_until: Optional[int] = None
        self.current_node: Optional[TreeNode] = None

    def is_free(self, current_tick: int):
        return self.blocked_until is None or current_tick >= self.blocked_until

    def work(self, node: TreeNode, current_tick: int):
        assert self.is_free(current_tick)
        self.blocked_until = current_tick + self.step_overhead + (ord(node.name) - 64)
        self.current_node = node

    def __repr__(self):
        current_node_name = self.current_node.name if self.current_node else None
        return f'Worker(blocked_until={self.blocked_until}, current_node={current_node_name})'


class WorkerGroup(object):
    def __init__(self, worker_count: int, step_overhead: int):
        self.workers = [Worker(step_overhead) for _ in range(worker_count)]

    def find_free_workers(self, current_tick: int):
        return list(w for w in self.workers if w.is_free(current_tick))

    @property
    def nodes_being_processed(self):
        return {w.current_node for w in self.workers if w.current_node is not None}

    def __repr__(self):
        return f'WorkerGroup(workers={self.workers})'


def calculate(text: str, worker_count: int = 5, step_overhead: int = 60) -> int:
    tree = build_tree(text)
    elapsed_ticks = 0
    workers = WorkerGroup(worker_count, step_overhead)
    already_seen = set()
    while len(already_seen) < len(tree):
        # find some available workers
        available_workers = workers.find_free_workers(elapsed_ticks)
        while len(available_workers) == 0:
            # no workers available, advance time
            elapsed_ticks += 1
            available_workers = workers.find_free_workers(elapsed_ticks)

        # check if the workers were processing something
        for worker in available_workers:
            if worker.current_node is not None:
                # add it to the already seen set
                already_seen.add(worker.current_node.name)

        if len(already_seen) == len(tree):
            # we're all done!
            break

        # pick next node
        available_nodes = (n for n in tree.values() if n.name not in already_seen and already_seen.issuperset(n.parents) and n not in workers.nodes_being_processed)
        available_nodes = sorted(available_nodes, key=lambda n: n.name)
        if len(available_nodes) == 0:
            # nothing to queue, advance time
            elapsed_ticks += 1
            continue

        for node, worker in zip(available_nodes[:len(available_workers)], available_workers):
            # process it
            worker.work(node, elapsed_ticks)

    return elapsed_ticks


puzzle = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip()
assert calculate(puzzle, worker_count=2, step_overhead=0) == 15
