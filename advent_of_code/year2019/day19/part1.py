from itertools import product

from .shared import create_drone_querier


def calculate(text: str) -> int:
    query_drone = create_drone_querier(text)
    return sum(query_drone(x, y) for x, y in product(range(50), range(50)))
