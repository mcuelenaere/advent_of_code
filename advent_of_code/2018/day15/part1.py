from .shared import parse_state, advance_state


def calculate(text: str) -> int:
    state = parse_state(text)
    rounds = 0
    was_full_round = True
    while was_full_round:
        state, was_full_round = advance_state(state)

        if was_full_round:
            # we only count full rounds
            rounds += 1

    return rounds * sum(c.hit_points for c in state.characters)


puzzle = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""".strip()
assert calculate(puzzle) == 27730

puzzle = """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""".strip()
assert calculate(puzzle) == 36334

puzzle = """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""".strip()
assert calculate(puzzle) == 39514

puzzle = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""".strip()
assert calculate(puzzle) == 27755

puzzle = """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""".strip()
assert calculate(puzzle) == 28944

puzzle = """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
""".strip()
assert calculate(puzzle) == 18740

