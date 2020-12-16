from enum import Enum
from typing import Dict, Tuple, List

Position = Tuple[int, int]
DIRECTIONS = (
    (0, -1),  # up
    (-1, 0),  # left
    (0, 1),   # down
    (1, 0),   # right
)


class State(Enum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3


def parse_text(text: str) -> Dict[Position, State]:
    infected_positions = {}
    for y, line in enumerate(text.splitlines()):
        middle = len(line) // 2
        x_offsets = {x for x, c in enumerate(line) if c == '#'}
        infected_positions.update({(x - middle, y - middle): State.INFECTED for x in x_offsets})
    return infected_positions


def infect(infection_states: Dict[Position, State], iterations: int, possible_states: List[State]) -> int:
    position = (0, 0)
    direction = 0
    number_of_new_infections = 0

    for _ in range(iterations):
        infection_state = infection_states.get(position, State.CLEAN)

        # calculate new direction
        if infection_state == State.CLEAN:
            direction += 1
        elif infection_state == State.INFECTED:
            direction -= 1
        elif infection_state == State.FLAGGED:
            direction += 2
        direction %= len(DIRECTIONS)

        # calculate new infection state
        new_infection_state = possible_states[(possible_states.index(infection_state) + 1) % len(possible_states)]

        if new_infection_state != State.CLEAN:
            infection_states[position] = new_infection_state
        else:
            del infection_states[position]

        if new_infection_state == State.INFECTED:
            number_of_new_infections += 1

        position = (position[0] + DIRECTIONS[direction][0], position[1] + DIRECTIONS[direction][1])

    return number_of_new_infections
