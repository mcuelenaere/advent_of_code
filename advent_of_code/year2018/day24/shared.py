import re
from enum import Enum
from typing import NamedTuple, Tuple, Set, Iterable, List, Optional


class Power(Enum):
    Bludgeoning = 'bludgeoning'
    Fire = 'fire'
    Cold = 'cold'
    Slashing = 'slashing'
    Radiation = 'radiation'


class BattleGroup(object):
    unit_count: int
    unit_hit_points: int
    immunities: Set[Power]
    weaknesses: Set[Power]
    attack: Power
    attack_points: int
    initiative_points: int

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def effective_power(self) -> int:
        return self.unit_count * self.attack_points

    def calculate_damage_for(self, other: 'BattleGroup') -> int:
        multiplier = 1
        if self.attack in other.immunities:
            multiplier = 0
        elif self.attack in other.weaknesses:
            multiplier = 2
        return self.effective_power * multiplier

    def __repr__(self):
        return f'BattleGroup(unit_hit_points={self.unit_hit_points}, unit_count={self.unit_count})'


BattleGroups = Tuple[BattleGroup, ...]


class BattleState(NamedTuple):
    immune_system: BattleGroups
    infection: BattleGroups

    @property
    def total_unit_count(self):
        return sum(g.unit_count for g in self.infection) + sum(g.unit_count for g in self.immune_system)


RE_BATTLE_GROUP = re.compile(r'(?P<units>\d+) units each with (?P<hit_points>\d+) hit points (\((?P<flags>[^)]+)\) )?with an attack that does (?P<attack_points>\d+) (?P<attack>\S+) damage at initiative (?P<initiative>\d+)')


def parse_groups(text: str) -> Iterable[BattleGroup]:
    for line in text.splitlines():
        m = RE_BATTLE_GROUP.match(line)
        if m is None:
            continue

        immunities = set()
        weaknesses = set()
        if m.group('flags'):
            for flag in m.group('flags').split('; '):
                powers = set(map(Power, flag.split(' to ')[1].split(', ')))
                if flag.startswith('immune to'):
                    immunities.update(powers)
                elif flag.startswith('weak to'):
                    weaknesses.update(powers)

        yield BattleGroup(
            unit_count=int(m.group('units')),
            unit_hit_points=int(m.group('hit_points')),
            immunities=immunities,
            weaknesses=weaknesses,
            attack=Power(m.group('attack')),
            attack_points=int(m.group('attack_points')),
            initiative_points=int(m.group('initiative'))
        )


def parse_battle_state(text: str) -> BattleState:
    immune_system, infection = text.split("\n\n")
    return BattleState(
        immune_system=tuple(parse_groups(immune_system)),
        infection=tuple(parse_groups(infection))
    )


def find_best_target(attacker: BattleGroup, defenders: BattleGroups) -> Optional[BattleGroup]:
    best_target = None
    most_damage = 0
    for defender in defenders:
        damage = attacker.calculate_damage_for(defender)
        if best_target is None or damage > most_damage:
            best_target = defender
            most_damage = damage
        elif damage == most_damage and defender.effective_power > best_target.effective_power:
            best_target = defender
            most_damage = damage
        elif damage == most_damage and defender.effective_power == best_target.effective_power and defender.initiative_points > best_target.initiative_points:
            best_target = defender
            most_damage = damage
    #print(attacker, 'would deal', best_target, 'damage', most_damage)
    return best_target if best_target is not None and most_damage > 0 else None


def pick_targets(attackers: BattleGroups, defenders: BattleGroups) -> List[Tuple[BattleGroup, BattleGroup]]:
    attackers = sorted(attackers, key=lambda g: (g.effective_power, g.initiative_points), reverse=True)
    targets = list()
    already_picked = list()
    for attacker in attackers:
        best_target = find_best_target(attacker, tuple(d for d in defenders if d not in already_picked))
        if best_target is not None:
            targets.append((attacker, best_target))
            already_picked.append(best_target)
    return targets


def attack(state: BattleState) -> BattleState:
    # target selection
    fights = pick_targets(state.infection, state.immune_system) + pick_targets(state.immune_system, state.infection)

    # sort
    fights = sorted(fights, key=lambda t: t[0].initiative_points, reverse=True)

    # attack
    for attacker, defender in fights:
        if attacker.unit_count <= 0:
            continue

        killed_units = min(attacker.calculate_damage_for(defender) // defender.unit_hit_points, defender.unit_count)
        #print(attacker, 'attacks', defender, 'killing', killed_units)
        defender.unit_count -= killed_units

    return BattleState(
        immune_system=tuple(g for g in state.immune_system if g.unit_count > 0),
        infection=tuple(g for g in state.infection if g.unit_count > 0),
    )
