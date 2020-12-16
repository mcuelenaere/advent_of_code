from .shared import parse_text, Program, Operation
from functools import wraps
from typing import Iterable, Callable


def memoize(fn: Callable[..., str]) -> Callable[..., str]:
    """
    Simple memoize function, which has an unbounded cache and expects the first argument of the wrapped function
    to be the cache key.
    """
    cache = {}

    @wraps(fn)
    def wrapper(key: str, *args) -> str:
        if key not in cache:
            cache[key] = fn(key, *args)
        return cache[key]

    return wrapper


@memoize
def do_dance(programs: str, dance: Iterable[Operation]) -> str:
    program = Program(programs)
    for step in dance:
        program.execute_operation(step)
    return str(program)


@memoize
def do_cycles(programs: str, dance: Iterable[Operation], amount: int) -> str:
    for _ in range(amount):
        programs = do_dance(programs, dance)
    return programs


def calculate(text: str) -> str:
    programs = ''.join(chr(x) for x in range(ord('a'), ord('p') + 1))
    dance = tuple(parse_text(text))
    for _ in range(1_000):
        programs = do_cycles(programs, dance, 1_000_000)
    return programs
