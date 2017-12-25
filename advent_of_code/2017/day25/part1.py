from .shared import parse_text


def calculate(text: str) -> int:
    diagnostic_checksum_iterations, turing_machine = parse_text(text)
    for _ in range(diagnostic_checksum_iterations):
        turing_machine.execute_step()
    return sum(turing_machine.tape.values())


puzzle = """
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
""".strip()
assert calculate(puzzle) == 3
