from itertools import product

from .shared import DroneQuerier, create_drone_querier


def iterate_tractor_beam_bounds(query_drone: DroneQuerier):
    # find starting point
    min_x, y = min((x, y) for x, y in product(range(10), range(10)) if query_drone(x, y) == 1 and (x, y) != (0, 0))
    max_x = min_x

    while True:
        while query_drone(min_x, y) == 0:
            min_x += 1
        max_x = max(max_x, min_x)
        while query_drone(max_x, y) == 1:
            max_x += 1
        if query_drone(max_x, y) == 0:
            max_x -= 1

        yield (min_x, y), (max_x, y)

        y += 1


def calculate(text: str):
    query_drone = create_drone_querier(text)

    last_lines = []
    for start, end in iterate_tractor_beam_bounds(query_drone):
        last_lines.append((start[0], end[0], start[1]))
        last_lines = last_lines[-100:]

        if len(last_lines) < 100:
            continue

        _, right, top = last_lines[-100]
        left, _, bottom = last_lines[-1]
        if right - left == 99 and bottom - top == 99:
            return left * 10000 + top
