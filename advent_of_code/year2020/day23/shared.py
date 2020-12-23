from typing import Sequence


class Node(object):
    __slots__ = ("next", "value")

    def __init__(self, next: "Node", value: int):
        self.next = next
        self.value = value

    def __repr__(self):
        return f"Node(value={self.value},next={self.next.value})"


def perform_rounds(cups: Sequence[int], rounds: int) -> Sequence[int]:
    nodes_by_value = dict()
    first_node = Node(next=None, value=cups[0])
    first_node.next = first_node
    nodes_by_value[cups[0]] = first_node
    last_node = first_node

    for n in cups[1:]:
        new_node = Node(next=first_node, value=n)
        nodes_by_value[n] = new_node
        last_node.next = new_node
        last_node = new_node

    current_node = first_node
    for _ in range(rounds):
        # extract 3 cups
        three_cups = (current_node.next, current_node.next.next, current_node.next.next.next)
        current_node.next = three_cups[2].next
        three_cups_values = tuple(n.value for n in three_cups)

        # find destination
        i = current_node.value - 1
        while i in three_cups_values or i <= 0:
            i -= 1
            if i <= 0:
                i = len(nodes_by_value)
        destination_node = nodes_by_value[i]

        # move 3 cups after destination
        destination_node.next, three_cups[2].next = three_cups[0], destination_node.next

        # move current cup
        current_node = current_node.next

    cups = []
    current_node = nodes_by_value[1]
    for _ in range(len(nodes_by_value)):
        cups.append(current_node.value)
        current_node = current_node.next

    return cups
