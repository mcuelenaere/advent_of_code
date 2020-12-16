from typing import List, NamedTuple


Node = NamedTuple("Node", children=List["Node"], metadata_entries=List[int])


def parse_tree(text: str) -> Node:
    items = tuple(int(x) for x in text.split(" "))

    root = None
    parents = []
    i = 0
    while i < len(items):
        child_node_count = items[i]
        metadata_count = items[i + 1]
        assert child_node_count >= 0
        assert metadata_count >= 0
        i += 2

        new_node = Node(children=[], metadata_entries=[])
        if root is None:
            # keep track of the root node
            root = new_node

        if len(parents) > 0:
            parent_node, parent_child_count, parent_metadata_count = parents.pop()
            # keep track of child
            parent_node.children.append(new_node)
            # decrease parent remaining child count
            parent_child_count -= 1
            # re-queue
            parents.append((parent_node, parent_child_count, parent_metadata_count))

        parents.append((new_node, child_node_count, metadata_count))

        # check if we need to parse parent's metadata entries
        while len(parents) > 0 and parents[-1][1] == 0:
            parent_node, _, parent_metadata_count = parents.pop()
            parent_node.metadata_entries.extend(items[i : i + parent_metadata_count])
            i += parent_metadata_count

    return root
