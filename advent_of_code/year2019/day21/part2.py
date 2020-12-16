from .shared import run_springdroid


def calculate(text: str) -> int:
    # (!A && D) || (!B && D) || (!C && D && H)
    springscript = "\n".join(
        [
            "NOT A J",
            "AND D J",
            "NOT B T",
            "AND D T",
            "OR T J",
            "NOT C T",
            "AND D T",
            "AND H T",
            "OR T J",
            "RUN",
        ]
    )
    return run_springdroid(text, springscript)
