from .shared import discover_map, shortest_path


def calculate(text: str) -> int:
    walls, oxygen_location = discover_map(text)
    path = shortest_path((0, 0), oxygen_location, walls)
    return len(path) - 1
