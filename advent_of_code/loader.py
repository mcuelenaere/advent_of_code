import os

from importlib import import_module
from typing import Any, Callable


def _read_file(filename: str) -> str:
    with open(filename, mode="r") as f:
        return f.read()


def load_puzzle_input(year: int, day: int) -> str:
    input_filename = os.path.join(
        os.path.dirname(__file__),
        "..",
        "puzzles",
        f"year{year}",
        f"day{day:02d}",
        "input.txt",
    )
    return _read_file(input_filename).strip("\n")


def load_puzzle_answer(year: int, day: int, part: int) -> str:
    answer_filename = os.path.join(
        os.path.dirname(__file__),
        "..",
        "puzzles",
        f"year{year}",
        f"day{day:02d}",
        f"answer-part{part}.txt",
    )
    return _read_file(answer_filename)


def load_puzzle_solver(year: int, day: int, part: int) -> Callable[[str], Any]:
    try:
        module = import_module(f"advent_of_code.year{year}.day{day:02d}.part{part}")  # type: Any
        if not hasattr(module, "calculate"):
            raise RuntimeError(f"Puzzle solution for year{year}-day{day}-part{part} has no calculate() method")
        return module.calculate
    except ImportError:
        raise RuntimeError(f"Could not find puzzle solution for year{year}-day{day}-part{part}")