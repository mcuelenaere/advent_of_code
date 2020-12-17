from typing import Iterable, Set, Tuple


Coordinate = Tuple[int, int, int, int]
Grid = Set[Coordinate]


def parse_grid(text: str) -> Grid:
    grid = set()
    z = 0
    w = 0
    for y, line in enumerate(text.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                grid.add((x, y, z, w))
    return grid


try:
    from .shared_native import neighbours
except ImportError:

    def neighbours(coordinate: Coordinate, enable_fourth_dimension: bool) -> Iterable[Coordinate]:
        for x in (coordinate[0], coordinate[0] + 1, coordinate[0] - 1):
            for y in (coordinate[1], coordinate[1] + 1, coordinate[1] - 1):
                for z in (coordinate[2], coordinate[2] + 1, coordinate[2] - 1):
                    w_combinations = (
                        (coordinate[3], coordinate[3] + 1, coordinate[3] - 1)
                        if enable_fourth_dimension
                        else (coordinate[3],)
                    )
                    for w in w_combinations:
                        if (x, y, z, w) != coordinate:
                            yield x, y, z, w


def perform_cycle(grid: Grid, enable_fourth_dimension: bool = False) -> Grid:
    new_grid = set()
    inactive_coordinates = set()
    for coordinate in grid:
        neighbour_count = 0
        for neighbour in neighbours(coordinate, enable_fourth_dimension):
            if neighbour in grid:
                neighbour_count += 1
            else:
                inactive_coordinates.add(neighbour)
        if neighbour_count in (2, 3):
            new_grid.add(coordinate)

    for coordinate in inactive_coordinates:
        neighbour_count = sum(1 for neighbour in neighbours(coordinate, enable_fourth_dimension) if neighbour in grid)
        if neighbour_count == 3:
            new_grid.add(coordinate)

    return new_grid


def print_grid(grid: Grid):
    min_x, max_x = min(map(lambda c: c[0], grid)), max(map(lambda c: c[0], grid))
    min_y, max_y = min(map(lambda c: c[1], grid)), max(map(lambda c: c[1], grid))
    z_values = sorted(set(map(lambda c: c[2], grid)))
    for z in z_values:
        print(f"z={z}")
        for y in range(min_y, max_y + 1):
            print("".join("#" if (x, y, z) in grid else "." for x in range(min_x, max_x + 1)))
