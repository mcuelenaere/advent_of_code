from .shared import find_point_of_convergence, parse_points


def calculate(text: str) -> int:
    points = tuple(parse_points(text))
    iteration, _ = find_point_of_convergence(points)
    return iteration
