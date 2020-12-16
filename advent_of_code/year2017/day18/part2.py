from threading import Thread
from time import sleep

from .shared import (
    CommunicatingProcessingUnit,
    ISndR,
    ISndV,
    QueueManager,
    parse_instructions,
)


class WorkerState(object):
    __slots__ = ("running", "sent_instructions")

    def __init__(self):
        self.running = True
        self.sent_instructions = 0

    def __repr__(self):
        return f"WorkerState(running={self.running}, sent_instructions={self.sent_instructions})"


def worker(cpu: CommunicatingProcessingUnit, state: WorkerState):
    while state.running:
        cur_instruction = cpu.instructions[cpu.instruction_offset]
        if isinstance(cur_instruction, ISndV) or isinstance(cur_instruction, ISndR):
            state.sent_instructions += 1
        cpu.execute_step()


def calculate(text: str) -> int:
    instructions = tuple(parse_instructions(text))
    queue_manager = QueueManager(2)

    # create CPUs
    cpu0 = CommunicatingProcessingUnit(instructions, program_id=0, other_program_id=1, queue_manager=queue_manager)
    cpu1 = CommunicatingProcessingUnit(instructions, program_id=1, other_program_id=0, queue_manager=queue_manager)

    # create states
    state0 = WorkerState()
    state1 = WorkerState()

    # create threads
    thread1 = Thread(target=worker, args=[cpu0, state0], name="cpu0")
    thread2 = Thread(target=worker, args=[cpu1, state1], name="cpu1")

    # start executing!
    thread1.start()
    thread2.start()

    # wait until both threads are blocked on each other
    sleep(1)
    while queue_manager.blocked_programs < 2:
        sleep(1)

    # tear down threads
    state0.running = False
    state1.running = False

    # send dummy messages to queues, to ensure any pending blocked threads will run at least 1 more instruction
    queue_manager.send_message(0, message=0)
    queue_manager.send_message(1, message=0)

    return state1.sent_instructions


puzzle = """
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
""".strip()
assert calculate(puzzle) == 3
