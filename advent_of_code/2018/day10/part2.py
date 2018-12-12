from .shared import parse_points, find_point_of_convergence


def calculate(text: str) -> int:
    points = tuple(parse_points(text))
    iteration, _ = find_point_of_convergence(points)
    return iteration
