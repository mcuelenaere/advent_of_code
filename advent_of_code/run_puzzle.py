#!/usr/bin/env python

import os

from importlib import import_module
from time import perf_counter
from typing import Any, Optional

import click


def read_file(filename: str) -> str:
    with open(filename, mode="r") as f:
        return f.read()


def format_duration(secs: float) -> str:
    if secs > 60:
        mins, secs = divmod(secs, 60)
        return f"{mins}m {secs:.2f}s"
    elif secs < 1:
        return f"{secs * 1e3:.2f}ms"
    else:
        return f"{secs:.2f}s"


def run_puzzle(year: int, day: int, part: int):
    # load puzzle
    puzzle_txt_filename = os.path.join(
        os.path.dirname(__name__),
        "advent_of_code",
        f"year{year}",
        f"day{day:02d}",
        "puzzle.txt",
    )
    try:
        puzzle = read_file(puzzle_txt_filename).strip("\n")
    except FileNotFoundError:
        print(f"Could not find puzzle for year{year}-day{day}")
        return

    try:
        module = import_module(f"advent_of_code.year{year}.day{day:02d}.part{part}")  # type: Any
    except ImportError:
        print(f"Could not find puzzle solution for year{year}-day{day}-part{part}")
        return

    if not hasattr(module, "calculate"):
        print(f"Puzzle solution for year{year}-day{day}-part{part} has no calculate() method")
        return

    t0 = perf_counter()
    result = module.calculate(puzzle)
    t1 = perf_counter()

    print(f"Result for puzzle year{year}-day{day}-part{part} is: {result}")
    print(f"\tsolving this took {format_duration(t1 - t0)}")
    print("")


@click.command()
@click.option("--year", type=int, default=2017)
@click.option("--day", type=int, default=None)
@click.option("--part", type=int, default=None)
def main(year: int, day: Optional[int], part: Optional[int]):
    def run_parts(year: int, day: int):
        if part is None:
            run_puzzle(year, day, part=1)
            run_puzzle(year, day, part=2)
        else:
            run_puzzle(year, day, part=part)

    if day is None:
        # run all the puzzles
        for day in range(1, 26):
            run_parts(year, day)
    else:
        # run the requested puzzle
        run_parts(year, day)


if __name__ == "__main__":
    main()
