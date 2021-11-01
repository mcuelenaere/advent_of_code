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


def _load_puzzle_solver_from_python(year: int, day: int, part: int) -> Callable[[str], Any]:
    module = import_module(f"advent_of_code.year{year}.day{day:02d}.part{part}")  # type: Any
    if not hasattr(module, "calculate"):
        raise ImportError(f"Puzzle solution for year{year}-day{day}-part{part} has no calculate() method")

    return module.calculate


def _load_puzzle_solver_from_rust(year: int, day: int, part: int) -> Callable[[str], Any]:
    module = import_module("aoc_rust")
    if not hasattr(module, f"year{year}"):
        raise ModuleNotFoundError(f"Module aoc_rust.year{year} not found")

    module = getattr(module, f"year{year}")
    if not hasattr(module, f"day{day:02d}"):
        raise ModuleNotFoundError(f"Module aoc_rust.year{year}.day{day:02d} not found")

    module = getattr(module, f"day{day:02d}")
    if not hasattr(module, f"part{part}"):
        raise ImportError(f"Puzzle solution for year{year}-day{day} has no part{part}() method")

    return getattr(module, f"part{part}")


def load_puzzle_solver(year: int, day: int, part: int) -> Callable[[str], Any]:
    try:
        return _load_puzzle_solver_from_python(year, day, part)
    except ImportError:
        # try loading from Rust
        return _load_puzzle_solver_from_rust(year, day, part)
