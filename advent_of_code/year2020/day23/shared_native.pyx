# distutils: language = c++

from libcpp.vector cimport vector


cdef struct Node:
    int value
    Node* next

def perform_rounds(list cups, int rounds):
    # pre-allocate all potential nodes
    cdef vector[Node] nodes
    for n in range(1, max(cups) + 1):
        nodes.push_back(Node(value=n, next=NULL))

    # initialize linked list
    cdef Node *first_node, *current_node, *new_node
    first_node = &nodes[cups[0] - 1]
    first_node.next = first_node
    current_node = first_node
    for n in cups[1:]:
        new_node = &nodes[n - 1]
        current_node.next, new_node.next = new_node, current_node.next
        current_node = new_node

    cdef Node *three_cups_1, *three_cups_2, *three_cups_3, *destination_node
    cdef int i
    with nogil:
        current_node = first_node
        for _ in range(rounds):
            # extract 3 cups
            three_cups_1 = current_node.next
            three_cups_2 = three_cups_1.next
            three_cups_3 = three_cups_2.next

            # remove them from the linked list
            current_node.next = three_cups_3.next

            # find destination
            i = current_node.value - 1
            while i == three_cups_1.value or i == three_cups_2.value or i == three_cups_3.value or i <= 0:
                i -= 1
                if i <= 0:
                    i = nodes.size()
            destination_node = &nodes[i - 1]

            # move 3 cups after destination
            destination_node.next, three_cups_3.next = three_cups_1, destination_node.next

            # move current cup
            current_node = current_node.next

    cups = []
    current_node = &nodes[0]
    for _ in range(nodes.size()):
        cups.append(current_node.value)
        current_node = current_node.next

    return cups
