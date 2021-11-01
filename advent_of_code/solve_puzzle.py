from advent_of_code.loader import load_puzzle_solver, load_puzzle_input
from time import perf_counter
from typing import Optional

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
    puzzle_input = load_puzzle_input(year, day)
    fn = load_puzzle_solver(year, day, part)

    t0 = perf_counter()
    result = fn(puzzle_input)
    t1 = perf_counter()

    print(f"Result for puzzle year{year}-day{day}-part{part} is: {result}")
    print(f"\tsolving this took {format_duration(t1 - t0)}")
    print("")


@click.command()
@click.option("--year", type=int, required=True)
@click.option("--day", type=int, default=None)
@click.option("--part", type=int, default=None)
def main(year: int, day: Optional[int], part: Optional[int]):
    def run_parts(day: int):
        if part is None:
            run_puzzle(year, day, part=1)
            run_puzzle(year, day, part=2)
        else:
            run_puzzle(year, day, part=part)

    if day is None:
        # run all the puzzles
        for day in range(1, 26):
            run_parts(day)
    else:
        # run the requested puzzle
        run_parts(day)


if __name__ == "__main__":
    main()
