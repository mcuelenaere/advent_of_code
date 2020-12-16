from typing import Iterable, List, Optional


class Node(object):
    __slots__ = ("next", "value")

    def __init__(self, value: int, next: Optional["Node"] = None):
        self.next = next
        self.value = value


class LinkedList(object):
    def __init__(self, iterable: Iterable[int] = ()):
        self.head = None
        self.tail = None
        for val in iterable:
            self.append(val)

    def append(self, value: int) -> Node:
        if self.tail is None:
            self.tail = Node(value)
            self.head = self.tail
        else:
            node = Node(value)
            self.tail.next = node
            self.tail = node

        return self.tail

    def append_after(self, value: int, node: Node) -> Node:
        new_node = Node(value)
        if node.next is not None:
            new_node.next = node.next
        node.next = new_node

        if self.tail is node:
            self.tail = new_node

        return new_node

    def __iter__(self):
        node = self.head
        yield node.value
        while node.next is not None:
            yield node.value
            node = node.next

    def __repr__(self):
        return f"LinkedList(head={self.head}, tail={self.tail})"


def spinlock(step_size: int, times: int) -> List[int]:
    buffer = LinkedList([0])
    node = buffer.tail
    for val in range(1, times + 1):
        for _ in range(step_size):
            if node.next is None:
                node = buffer.head
            else:
                node = node.next
        node = buffer.append_after(val, node)
    return list(buffer)
