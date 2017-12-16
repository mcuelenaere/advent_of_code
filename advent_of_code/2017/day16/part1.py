from .shared import parse_text, Program


def calculate(text: str, programs: str = None) -> str:
    if programs is None:
        # default value
        programs = ''.join(chr(x) for x in range(ord('a'), ord('p') + 1))

    program = Program(programs)
    for operation in parse_text(text):
        program.execute_operation(operation)
    return str(program)


assert calculate('s1', 'abcde') == 'eabcd'
assert calculate('s1,x3/4', 'abcde') == 'eabdc'
assert calculate('s1,x3/4,pe/b', 'abcde') == 'baedc'
