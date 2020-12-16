from typing import Optional

from .shared import CharacterType, State, advance_state, parse_state


def count_elves(state: State) -> int:
    return sum(1 for c in state.characters if c.type == CharacterType.Elf)


def try_battle(text: str, elf_attack_power: int) -> Optional[int]:
    state = parse_state(text, elf_attack_power=elf_attack_power, goblin_attack_power=3)
    number_of_elves = count_elves(state)
    rounds = 0
    was_full_round = True
    while was_full_round:
        state, was_full_round = advance_state(state)
        if count_elves(state) < number_of_elves:
            # we lost an elf :(
            return None

        if was_full_round:
            # we only count full rounds
            rounds += 1

    # battle is over and all our elves are still alive!
    return rounds * sum(c.hit_points for c in state.characters)


def calculate(text: str) -> int:
    # try finding the upper bound first
    has_won = False
    cur_power = 4
    cur_outcome = None
    while not has_won:
        cur_outcome = try_battle(text, cur_power)
        has_won = cur_outcome is not None
        if not has_won:
            cur_power *= 2

    # now try finding the exact minimum, using a binary search
    lower = int(cur_power / 2)
    upper = cur_power
    upper_outcome = cur_outcome
    while upper - lower > 1:
        mid = int((lower + upper) / 2)
        outcome = try_battle(text, mid)
        has_won = outcome is not None
        if has_won:
            upper = mid
            upper_outcome = outcome
        else:
            lower = mid

    return upper_outcome


puzzle = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
""".strip()
assert calculate(puzzle) == 4988

puzzle = """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""".strip()
assert calculate(puzzle) == 31284

puzzle = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""".strip()
assert calculate(puzzle) == 3478

puzzle = """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""".strip()
assert calculate(puzzle) == 6474

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
assert calculate(puzzle) == 1140
