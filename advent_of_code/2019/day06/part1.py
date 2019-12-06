from .shared import parse_graph, construct_path_to_origin


def calculate(text: str) -> int:
    graph = parse_graph(text)

    # count number of direct and indirect orbits
    number_of_orbits = 0
    for object in graph.keys():
        number_of_orbits += sum(1 for _ in construct_path_to_origin(graph, object))

    return number_of_orbits


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
K)L"""
assert calculate(puzzle) == 42
