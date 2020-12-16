from collections import deque

from ..day05.shared import parse_instructions, streaming_evaluate


class Computer(object):
    def __init__(self, instructions_str: str, nic_number: int):
        instructions = parse_instructions(instructions_str)
        self._cpu = streaming_evaluate(instructions)
        self._nic_number = nic_number
        self._input_queue = deque()
        self._initialized = False
        self.is_running = True

    def run_iteration(self):
        if not self.is_running:
            return

        if not self._initialized:
            next(self._cpu)
            self._cpu.send(self._nic_number)
            self._initialized = True

        def receive_message(addr: int):
            x = next(self._cpu)
            y = next(self._cpu)
            yield addr, x, y

        def try_sending_message(x: int, y: int, skip_first: bool = False):
            if not skip_first:
                res = self._cpu.send(x)
                if res is not None:
                    yield from receive_message(res)
                    yield from try_sending_message(x, y, False)
                    return
            res = self._cpu.send(y)
            if res is not None:
                yield from receive_message(res)
                yield from try_sending_message(x, y, True)

        try:
            if len(self._input_queue) > 0:
                while len(self._input_queue) > 0:
                    x, y = self._input_queue.popleft()
                    yield from try_sending_message(x, y)
            else:
                res = self._cpu.send(-1)
                if res is not None:
                    yield from receive_message(res)
        except StopIteration:
            self.is_running = False
            return

    def queue_packet(self, x: int, y: int):
        self._input_queue.append((x, y))

    def queue_length(self) -> int:
        return len(self._input_queue)
