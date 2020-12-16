from .shared import discover_map, flood_region


def calculate(text: str) -> int:
    walls, oxygen_location = discover_map(text)
    return flood_region(walls, oxygen_location)
