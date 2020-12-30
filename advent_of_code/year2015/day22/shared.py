import math

from typing import List, NamedTuple, Optional, Type

from ..day21.shared import Character, CharacterType, parse_character  # noqa: F401


class BattleState(NamedTuple):
    player: Character
    enemy: Character
    active_character: CharacterType
    player_mana: int
    active_effects: List["_Effect"]

    def winning_party(self) -> Optional[CharacterType]:
        if self.player.hit_points <= 0:
            return CharacterType.ENEMY
        elif self.enemy.hit_points <= 0:
            return CharacterType.PLAYER
        else:
            return None

    def next_state(self, spell: Optional["_Spell"] = None) -> Optional["BattleState"]:
        state = self

        assert state.winning_party() is None

        # apply effects' turn start
        effects = state.active_effects
        for effect in effects:
            state = effect.turn_start(state)

        # reduce effect timers for previously active effects
        new_effects = [e.decremented_with(1) for e in effects]

        # apply wear-off for effects that ended
        for effect in new_effects:
            if effect.timer == 0:
                state = effect.effect_off(state)

        # remove effects that have ended
        new_effects = [e for e in new_effects if e.timer > 0]
        state = state._replace(active_effects=new_effects)

        if state.active_character == CharacterType.PLAYER and state.player.hit_points > 0:
            assert spell is not None

            # check if spell can be cast
            if not spell.can_apply(state) or state.player_mana < spell.cost:
                return None

            # cast spell
            state = state._replace(player_mana=state.player_mana - spell.cost)
            state = spell.apply(state)
        elif state.active_character == CharacterType.ENEMY and state.enemy.hit_points > 0:
            assert spell is None

            # deal damage
            damage = max(state.enemy.damage_score - state.player.armor_score, 1)
            new_player = state.player._replace(hit_points=state.player.hit_points - damage)
            state = state._replace(player=new_player)

        # flip active character
        state = state._replace(active_character=state.active_character.opposite())

        return state


class _Effect(object):
    duration: int

    def __init__(self, timer: int = None):
        self.timer = self.duration if timer is None else timer

    def turn_start(self, state: BattleState) -> BattleState:
        return state

    def effect_on(self, state: BattleState) -> BattleState:
        return state

    def effect_off(self, state: BattleState) -> BattleState:
        return state

    @property
    def name(self):
        return self.__class__.__name__.replace("Effect", "")

    def decremented_with(self, decrement: int) -> "_Effect":
        return type(self)(self.timer - decrement)

    def __repr__(self):
        return f"{self.name}(timer={self.timer})"


class ShieldEffect(_Effect):
    duration = 6

    def effect_on(self, state: BattleState):
        new_player = state.player._replace(armor_score=state.player.armor_score + 7)
        return state._replace(player=new_player)

    def effect_off(self, state: BattleState):
        new_player = state.player._replace(armor_score=state.player.armor_score - 7)
        return state._replace(player=new_player)


class PoisonEffect(_Effect):
    duration = 6

    def turn_start(self, state: BattleState):
        new_enemy = state.enemy._replace(hit_points=state.enemy.hit_points - 3)
        return state._replace(enemy=new_enemy)


class RechargeEffect(_Effect):
    duration = 5

    def turn_start(self, state: BattleState):
        return state._replace(player_mana=state.player_mana + 101)


class DifficultyHardEffect(_Effect):
    duration = math.inf

    def turn_start(self, state: BattleState):
        new_player = state.player._replace(hit_points=state.player.hit_points - 1)
        return state._replace(player=new_player)


class _Spell(object):
    cost: int

    def can_apply(self, state: BattleState) -> bool:
        return True

    def apply(self, state: BattleState):
        raise NotImplementedError()

    @property
    def name(self):
        return self.__class__.__name__.replace("Spell", "")

    def __repr__(self):
        return f"<{self.name}>"


class MagicMissileSpell(_Spell):
    cost = 53

    def apply(self, state: BattleState):
        new_enemy = state.enemy._replace(hit_points=state.enemy.hit_points - 4)
        return state._replace(enemy=new_enemy)


class DrainSpell(_Spell):
    cost = 73

    def apply(self, state: BattleState):
        new_enemy = state.enemy._replace(hit_points=state.enemy.hit_points - 2)
        new_player = state.player._replace(hit_points=state.player.hit_points + 2)
        return state._replace(enemy=new_enemy, player=new_player)


class _EffectSpell(_Spell):
    def __init__(self, effect_type: Type[_Effect]):
        self.effect_type = effect_type

    def can_apply(self, state: BattleState):
        active_effect_types = {type(e) for e in state.active_effects}
        return self.effect_type not in active_effect_types

    def apply(self, state: BattleState):
        effect = self.effect_type()
        state = effect.effect_on(state)
        new_active_effects = state.active_effects + [effect]
        return state._replace(active_effects=new_active_effects)


class ShieldSpell(_EffectSpell):
    cost = 113

    def __init__(self):
        super(ShieldSpell, self).__init__(ShieldEffect)


class PoisonSpell(_EffectSpell):
    cost = 173

    def __init__(self):
        super(PoisonSpell, self).__init__(PoisonEffect)


class RechargeSpell(_EffectSpell):
    cost = 229

    def __init__(self):
        super(RechargeSpell, self).__init__(RechargeEffect)


SPELLS = (
    MagicMissileSpell(),
    DrainSpell(),
    ShieldSpell(),
    PoisonSpell(),
    RechargeSpell(),
)


# tests
_state = BattleState(
    player=Character(hit_points=10, damage_score=0, armor_score=0),
    enemy=Character(hit_points=13, damage_score=8, armor_score=0),
    active_character=CharacterType.PLAYER,
    player_mana=250,
    active_effects=[],
)
_state = _state.next_state(spell=PoisonSpell())
_state = _state.next_state()
_state = _state.next_state(spell=MagicMissileSpell())
_state = _state.next_state()
assert _state.winning_party() == CharacterType.PLAYER


_state = BattleState(
    player=Character(hit_points=10, damage_score=0, armor_score=0),
    enemy=Character(hit_points=14, damage_score=8, armor_score=0),
    active_character=CharacterType.PLAYER,
    player_mana=250,
    active_effects=[],
)
_state = _state.next_state(spell=RechargeSpell())
_state = _state.next_state()
_state = _state.next_state(spell=ShieldSpell())
_state = _state.next_state()
_state = _state.next_state(spell=DrainSpell())
_state = _state.next_state()
_state = _state.next_state(spell=PoisonSpell())
_state = _state.next_state()
_state = _state.next_state(spell=MagicMissileSpell())
_state = _state.next_state()
assert _state.winning_party() == CharacterType.PLAYER


SearchState = NamedTuple("SearchState", battle_state=BattleState, spent_mana=int)


def find_win_for_lowest_spent_mana(initial_state: BattleState):
    queue = [SearchState(battle_state=initial_state, spent_mana=0)]
    lowest_mana_spent = None

    while len(queue) > 0:
        current_state, current_spent_mana = queue.pop()
        if lowest_mana_spent is not None and current_spent_mana > lowest_mana_spent:
            # prune this branch
            continue

        while current_state.winning_party() is None:
            if current_state.active_character == CharacterType.ENEMY:
                current_state = current_state.next_state()
            elif current_state.active_character == CharacterType.PLAYER:
                for spell in SPELLS:
                    new_state = current_state.next_state(spell=spell)
                    if new_state is None or new_state.winning_party() == CharacterType.ENEMY:
                        # spell can't be cast or it results in player death, skip it
                        continue

                    queue.append(
                        SearchState(
                            battle_state=new_state,
                            spent_mana=current_spent_mana + spell.cost,
                        )
                    )
                break

        if current_state.winning_party() == CharacterType.PLAYER and (
            lowest_mana_spent is None or current_spent_mana < lowest_mana_spent
        ):
            lowest_mana_spent = current_spent_mana

    return lowest_mana_spent
