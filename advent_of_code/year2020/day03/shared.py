from typing import Tuple, Set

Trees = Set[Tuple[int, int]]


def parse_map(text: str) -> Tuple[int, int, Trees]:
    max_x = 0
    y = 0
    trees = set()
    for line in text.splitlines():
        max_x = len(line)
        for x, char in enumerate(line, start=0):
            if char == '#':
                trees.add((x, y))
        y += 1
    return max_x, y, trees


def count_trees_for_slope_pattern(max_x: int, max_y: int, trees: Trees, slope_pattern: Tuple[int, int]) -> int:
    player_x = 0
    player_y = 0
    seen_trees = 0
    while player_y < max_y:
        if (player_x % max_x, player_y) in trees:
            seen_trees += 1
        player_x += slope_pattern[0]
        player_y += slope_pattern[1]
    return seen_trees
