from .shared import construct_path_to_origin, parse_graph


def calculate(text: str) -> int:
    graph = parse_graph(text)

    # find path of YOU to COM
    our_path = tuple(construct_path_to_origin(graph, "YOU"))
    santa_path = tuple(construct_path_to_origin(graph, "SAN"))

    # find common object between both paths
    for our_idx, object in enumerate(our_path):
        try:
            santa_idx = santa_path.index(object)
        except ValueError:
            continue

        # count the number of orbital transfers
        return our_idx + santa_idx


puzzle = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
assert calculate(puzzle) == 4
