from .shared import count_trees_for_slope_pattern, parse_map


def calculate(text: str) -> int:
    max_x, max_y, trees = parse_map(text)
    return count_trees_for_slope_pattern(max_x, max_y, trees, slope_pattern=(3, 1))


puzzle = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
assert calculate(puzzle) == 7
