from .shared import attack, parse_battle_state


def calculate(text: str) -> int:
    boost = 1
    has_won = False
    while not has_won:
        state = parse_battle_state(text)
        # apply boost
        for group in state.immune_system:
            group.attack_points += boost

        # fight till the death (or until we reached an equilibrum)
        while len(state.infection) > 0 and len(state.immune_system) > 0:
            prev_count = state.total_unit_count
            state = attack(state)
            cur_count = state.total_unit_count
            if cur_count == prev_count:
                # we're stuck
                break
        has_won = len(state.immune_system) > 0 and len(state.infection) == 0
        boost += 1
    return state.total_unit_count


puzzle = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".strip()
assert calculate(puzzle) == 51
