from enum import Enum
from itertools import combinations, product
from typing import NamedTuple, Tuple, Iterable

Character = NamedTuple('Character', hit_points=int, damage_score=int, armor_score=int)
Item = NamedTuple('Item', name=str, cost=int, damage=int, armor=int)
ShopCategory = NamedTuple('ShopCategory', name=str, items=Tuple[Item, ...], min_amount=int, max_amount=int)
Shop = NamedTuple('Shop', categories=Tuple[ShopCategory, ...])

SHOP = Shop(
    categories=(
        ShopCategory(
            name='weapon',
            min_amount=1,
            max_amount=1,
            items=(
                Item(name='Dagger', cost=8, damage=4, armor=0),
                Item(name='Shortsword', cost=10, damage=5, armor=0),
                Item(name='Warhammer', cost=25, damage=6, armor=0),
                Item(name='Longsword', cost=40, damage=7, armor=0),
                Item(name='Greataxe', cost=74, damage=8, armor=0),
            )
        ),
        ShopCategory(
            name='armor',
            min_amount=0,
            max_amount=1,
            items=(
                Item(name='Leather', cost=13, damage=0, armor=1),
                Item(name='Chainmail', cost=31, damage=0, armor=2),
                Item(name='Splintmail', cost=53, damage=0, armor=3),
                Item(name='Bandedmail', cost=75, damage=0, armor=4),
                Item(name='Platemail', cost=102, damage=0, armor=5),
            )
        ),
        ShopCategory(
            name='ring',
            min_amount=0,
            max_amount=2,
            items=(
                Item(name='Damage +1', cost=25, damage=1, armor=0),
                Item(name='Damage +2', cost=50, damage=2, armor=0),
                Item(name='Damage +3', cost=100, damage=3, armor=0),
                Item(name='Defense +1', cost=20, damage=0, armor=1),
                Item(name='Defense +2', cost=40, damage=0, armor=2),
                Item(name='Defense +3', cost=80, damage=0, armor=3),
            )
        ),
    )
)


def parse_character(text: str) -> Character:
    for line in text.splitlines():
        label, value = line.split(":", 2)
        if label == 'Hit Points':
            hit_points = int(value)
        elif label == 'Damage':
            damage = int(value)
        elif label == 'Armor':
            armor = int(value)
    return Character(hit_points=hit_points, damage_score=damage, armor_score=armor)


class CharacterType(Enum):
    PLAYER = 'PLAYER'
    ENEMY = 'ENEMY'

    def opposite(self):
        if self == self.PLAYER:
            return self.ENEMY
        else:
            return self.PLAYER


def calculate_winner(player: Character, enemy: Character) -> CharacterType:
    parties = {
        CharacterType.PLAYER: player,
        CharacterType.ENEMY: enemy,
    }
    attacker = CharacterType.PLAYER
    while parties[CharacterType.PLAYER].hit_points > 0 and parties[CharacterType.ENEMY].hit_points > 0:
        defender = attacker.opposite()

        # deal damage
        damage = max(parties[attacker].damage_score - parties[defender].armor_score, 1)
        parties[defender] = parties[defender]._replace(hit_points=parties[defender].hit_points - damage)

        # flip sides
        attacker = attacker.opposite()

    for type, party in parties.items():
        if party.hit_points > 0:
            return type


_enemy = parse_character("""
Hit Points: 12
Damage: 7
Armor: 2
""".strip())
_player = parse_character("""
Hit Points: 8
Damage: 5
Armor: 5
""".strip())
assert calculate_winner(_player, _enemy) == CharacterType.PLAYER


def all_shop_combinations():
    possible_combinations = []
    for category in SHOP.categories:
        # calculate all combinations within this category
        category_combinations = []
        for length in range(category.min_amount, category.max_amount + 1):
            category_combinations.extend(combinations(category.items, length))
        possible_combinations.append(tuple(category_combinations))
    return tuple(product(*possible_combinations))


def build_character_from_items(hit_points: int, items: Iterable[Item]) -> Tuple[Character, int]:
    damage_score = 0
    armor_score = 0
    total_cost = 0
    for item in items:
        damage_score += item.damage
        armor_score += item.armor
        total_cost += item.cost

    return Character(hit_points=hit_points, damage_score=damage_score, armor_score=armor_score), total_cost
