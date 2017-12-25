import re
from enum import Enum
from typing import Dict, NamedTuple, Tuple


class MoveDirection(Enum):
    LEFT = 'left'
    RIGHT = 'right'


class Step(NamedTuple):
    write_value: int
    move_direction: MoveDirection
    next_state: str


State = Tuple[Step, Step]

RE_INITIAL_STATE = re.compile(r'^Begin in state ([A-Z]).$')
RE_DIAGNOSTIC_CHECKSUM = re.compile(r'^Perform a diagnostic checksum after (\d+) steps.$')
RE_IN_STATE = re.compile(r'^In state ([A-Z]):$')
RE_IF_CURRENT_VALUE = re.compile(r'^\s*If the current value is ([01]):$')
RE_WRITE_VALUE = re.compile(r'^\s*- Write the value ([01]).$')
RE_MOVE_SLOT = re.compile(r'^\s*- Move one slot to the (left|right).$')
RE_CONTINUE_STATE = re.compile(r'^\s*- Continue with state ([A-Z]).$')


def parse_text(text: str) -> Tuple[int, 'TuringMachine']:
    lines = text.splitlines()

    def match(regex):
        line = lines.pop(0)
        m = regex.match(line)
        if m is None:
            raise ValueError(f'Could not parse line "{line}"')
        return m.groups()[0]

    initial_state = match(RE_INITIAL_STATE)
    diagnostic_checksum_iterations = int(match(RE_DIAGNOSTIC_CHECKSUM))
    states = {}

    while len(lines) > 0:
        lines.pop(0)
        state_name = match(RE_IN_STATE)
        steps = []
        for _ in range(2):
            _ = match(RE_IF_CURRENT_VALUE)
            write_value = int(match(RE_WRITE_VALUE))
            slot_direction = MoveDirection(match(RE_MOVE_SLOT))
            next_state = match(RE_CONTINUE_STATE)
            steps.append(Step(
                write_value=write_value,
                move_direction=slot_direction,
                next_state=next_state
            ))

        states[state_name] = tuple(steps)

    return diagnostic_checksum_iterations, TuringMachine(initial_state, states)


class TuringMachine(object):
    def __init__(self, initial_state: str, states: Dict[str, State]):
        self.tape = {}
        self.cursor = 0
        self.current_state = initial_state
        self.states = states

    def execute_step(self):
        # determine step
        step_if_zero, step_if_one = self.states[self.current_state]
        step = step_if_zero if self.tape.get(self.cursor, 0) == 0 else step_if_one

        # execute step
        self.tape[self.cursor] = step.write_value
        self.cursor += 1 if step.move_direction == MoveDirection.RIGHT else -1
        self.current_state = step.next_state

    def __repr__(self):
        return f'TuringMachine(tape={self.tape}, cursor={self.cursor}, current_state={self.current_state})'
