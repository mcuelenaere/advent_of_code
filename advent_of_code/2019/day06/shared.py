from typing import Dict


Graph = Dict[str, str]


def parse_graph(text: str) -> Graph:
    # construct directed graph
    graph = {}
    for line in text.splitlines():
        left, right = line.split(")")
        graph[right] = left
    return graph


def construct_path_to_origin(graph: Graph, start: str):
    cur = start
    while cur in graph:
        cur = graph[cur]
        yield cur
