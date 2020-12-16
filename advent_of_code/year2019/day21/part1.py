from .shared import run_springdroid


def calculate(text: str) -> int:
    # (!A && D) || (!B && D) || (!C && D)
    springscript = "\n".join([
        'NOT A J',
        'AND D J',
        'NOT B T',
        'AND D T',
        'OR T J',
        'NOT C T',
        'AND D T',
        'OR T J',
        'WALK',
    ])
    return run_springdroid(text, springscript)
