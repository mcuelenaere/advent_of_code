import re
from collections import defaultdict
from queue import Queue
from threading import Lock
from typing import NamedTuple, Iterator, Union, Tuple


ISndV = NamedTuple('ISndV', value=int)
ISetV = NamedTuple('ISetV', dst_register=str, src_value=int)
IAddV = NamedTuple('IAddV', dst_register=str, src_value=int)
IMulV = NamedTuple('IMulV', dst_register=str, src_value=int)
IModV = NamedTuple('IModV', dst_register=str, src_value=int)
ISndR = NamedTuple('ISndR', src_register=str)
ISetR = NamedTuple('ISetR', dst_register=str, src_register=str)
IAddR = NamedTuple('IAddR', dst_register=str, src_register=str)
IMulR = NamedTuple('IMulR', dst_register=str, src_register=str)
IModR = NamedTuple('IModR', dst_register=str, src_register=str)
IJgzRR = NamedTuple('IJgzRR', cnd_register=str, jump_register=str)
IJgzRV = NamedTuple('IJgzRV', cnd_register=str, jump_offset=int)
IJgzVV = NamedTuple('IJgzVV', cnd_value=int, jump_offset=int)
IRcv = NamedTuple('IRcv', dst_register=str)
Instruction = Union[ISndV, ISndR, ISetV, ISetR, IAddV, IAddR, IMulV, IMulR, IModV, IModR, IRcv, IJgzRR, IJgzRV, IJgzVV]


REGEXES = (
    (re.compile(r'^snd (?P<value>-?\d+)$'), ISndV),
    (re.compile(r'^snd (?P<src_register>[a-z]+)$'), ISndR),
    (re.compile(r'^set (?P<dst_register>[a-z]) (?P<src_value>-?\d+)$'), ISetV),
    (re.compile(r'^add (?P<dst_register>[a-z]) (?P<src_value>-?\d+)$'), IAddV),
    (re.compile(r'^mul (?P<dst_register>[a-z]) (?P<src_value>-?\d+)$'), IMulV),
    (re.compile(r'^mod (?P<dst_register>[a-z]) (?P<src_value>-?\d+)$'), IModV),
    (re.compile(r'^set (?P<dst_register>[a-z]) (?P<src_register>[a-z]+)$'), ISetR),
    (re.compile(r'^add (?P<dst_register>[a-z]) (?P<src_register>[a-z]+)$'), IAddR),
    (re.compile(r'^mul (?P<dst_register>[a-z]) (?P<src_register>[a-z]+)$'), IMulR),
    (re.compile(r'^mod (?P<dst_register>[a-z]) (?P<src_register>[a-z]+)$'), IModR),
    (re.compile(r'^rcv (?P<dst_register>[a-z])$'), IRcv),
    (re.compile(r'^jgz (?P<cnd_register>[a-z]) (?P<jump_offset>-?\d+)$'), IJgzRV),
    (re.compile(r'^jgz (?P<cnd_value>-?\d+) (?P<jump_offset>-?\d+)$'), IJgzVV),
    (re.compile(r'^jgz (?P<cnd_register>[a-z]) (?P<jump_register>[a-z])$'), IJgzRR),
)


def parse_instructions(text: str) -> Iterator[Instruction]:
    for line in text.splitlines():
        instruction = None
        for regex, instruction_type in REGEXES:
            m = regex.match(line)
            if m:
                args = {k: instruction_type.__annotations__[k](v) for k, v in m.groupdict().items()}
                instruction = instruction_type(**args)
                break

        if instruction:
            yield instruction
        else:
            raise ValueError(f'Could not parse line "{line}')


class ProcessingMixin(object):
    __slots__ = ('registers', 'instructions', 'instruction_offset', 'playing_frequency', 'recovered_frequency')

    def __init__(self, instructions: Tuple[Instruction, ...]):
        self.registers = defaultdict(int)
        self.instructions = instructions
        self.instruction_offset = 0

    def _execute_instruction(self, instruction: Instruction):
        if isinstance(instruction, ISetV):
            self.registers[instruction.dst_register] = instruction.src_value
            self.instruction_offset += 1
        elif isinstance(instruction, IAddV):
            self.registers[instruction.dst_register] += instruction.src_value
            self.instruction_offset += 1
        elif isinstance(instruction, IMulV):
            self.registers[instruction.dst_register] *= instruction.src_value
            self.instruction_offset += 1
        elif isinstance(instruction, IModV):
            self.registers[instruction.dst_register] %= instruction.src_value
            self.instruction_offset += 1
        elif isinstance(instruction, ISetR):
            self.registers[instruction.dst_register] = self.registers[instruction.src_register]
            self.instruction_offset += 1
        elif isinstance(instruction, IAddR):
            self.registers[instruction.dst_register] += self.registers[instruction.src_register]
            self.instruction_offset += 1
        elif isinstance(instruction, IMulR):
            self.registers[instruction.dst_register] *= self.registers[instruction.src_register]
            self.instruction_offset += 1
        elif isinstance(instruction, IModR):
            self.registers[instruction.dst_register] %= self.registers[instruction.src_register]
            self.instruction_offset += 1
        elif isinstance(instruction, IJgzRV):
            self.instruction_offset += instruction.jump_offset if self.registers[instruction.cnd_register] > 0 else 1
        elif isinstance(instruction, IJgzRR):
            self.instruction_offset += self.registers[instruction.jump_register] if self.registers[instruction.cnd_register] > 0 else 1
        elif isinstance(instruction, IJgzVV):
            self.instruction_offset += instruction.jump_offset if instruction.cnd_value > 0 else 1
        else:
            raise ValueError(f'Unknown instruction {instruction}')

    def execute_step(self):
        self._execute_instruction(self.instructions[self.instruction_offset])


class MusicProcessingUnit(ProcessingMixin):
    __slots__ = ('playing_frequency', 'recovered_frequency')

    def __init__(self, instructions: Tuple[Instruction, ...]):
        super().__init__(instructions)
        self.playing_frequency = None
        self.recovered_frequency = None

    def _execute_instruction(self, instruction: Instruction):
        if isinstance(instruction, ISndV):
            self.playing_frequency = instruction.value
            self.instruction_offset += 1
        elif isinstance(instruction, ISndR):
            self.playing_frequency = self.registers[instruction.src_register]
            self.instruction_offset += 1
        elif isinstance(instruction, IRcv):
            if self.registers[instruction.dst_register] != 0:
                self.recovered_frequency = self.playing_frequency
            self.instruction_offset += 1
        else:
            super()._execute_instruction(instruction)


class QueueManager(object):
    def __init__(self, program_count: int):
        self._queues = {i: Queue() for i in range(program_count)}
        self._blocked_programs = 0
        self._lock = Lock()

    def send_message(self, destination_id: int, message: int):
        self._queues[destination_id].put_nowait(message)

    def receive_message(self, program_id: int) -> int:
        with self._lock:
            self._blocked_programs += 1
        try:
            return self._queues[program_id].get(block=True)
        finally:
            with self._lock:
                self._blocked_programs -= 1

    @property
    def blocked_programs(self):
        with self._lock:
            return self._blocked_programs


class CommunicatingProcessingUnit(ProcessingMixin):
    __slots__ = ('message_queue', 'program_id', 'other_program_id', 'queue_manager')

    def __init__(self, instructions: Tuple[Instruction, ...], program_id: int, other_program_id: int, queue_manager: QueueManager):
        super().__init__(instructions)
        self.queue_manager = queue_manager
        self.program_id = program_id
        self.other_program_id = other_program_id
        self.registers['p'] = program_id

    def _execute_instruction(self, instruction: Instruction):
        if isinstance(instruction, ISndV):
            self.queue_manager.send_message(self.other_program_id, instruction.value)
            self.instruction_offset += 1
        elif isinstance(instruction, ISndR):
            self.queue_manager.send_message(self.other_program_id, self.registers[instruction.src_register])
            self.instruction_offset += 1
        elif isinstance(instruction, IRcv):
            self.registers[instruction.dst_register] = self.queue_manager.receive_message(self.program_id)
            self.instruction_offset += 1
        else:
            super()._execute_instruction(instruction)
