from ..day05.shared import streaming_evaluate
from typing import Iterable


def run_amplifier(text: str, phase_settings: Iterable[int]) -> int:
    last_output_signal = 0
    for phase_setting in phase_settings:
        instructions = list(map(int, text.strip().split(',')))
        gen = streaming_evaluate(instructions)
        next(gen)
        gen.send(phase_setting)
        last_output_signal = gen.send(last_output_signal)
    return last_output_signal


assert run_amplifier("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", (4, 3, 2, 1, 0)) == 43210


def run_amplifier_feedback_loop(text: str, phase_settings: Iterable[int]) -> int:
    def construct_amplifier(phase_setting: int):
        instructions = list(map(int, text.strip().split(',')))
        gen = streaming_evaluate(instructions)
        next(gen)
        gen.send(phase_setting)
        return gen

    amplifiers = tuple(construct_amplifier(phase_setting) for phase_setting in phase_settings)

    last_output = 0
    while True:
        try:
            for amplifier in amplifiers:
                ret = amplifier.send(last_output)
                if ret is None:
                    ret = amplifier.send(last_output)
                last_output = ret
        except StopIteration:
            break
    return last_output


assert run_amplifier_feedback_loop("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5", (9, 8, 7, 6, 5)) == 139629729
