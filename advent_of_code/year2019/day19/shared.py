from typing import Callable

from ..day05.shared import parse_instructions, streaming_evaluate


DroneQuerier = Callable[[int, int], int]


def create_drone_querier(text: str) -> Callable[[int, int], int]:
    instructions = parse_instructions(text)

    def query_drone(x: int, y: int) -> int:
        assert x >= 0
        assert y >= 0
        gen = streaming_evaluate(instructions)
        next(gen)
        gen.send(x)
        return gen.send(y)

    return query_drone
