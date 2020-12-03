#!/usr/bin/env python

import click
import os

from importlib import import_module
from typing import Optional


def read_file(filename: str) -> str:
    with open(filename, mode='r') as f:
        return f.read()


def run_puzzle(year: int, day: int, part: int):
    # load puzzle
    puzzle_txt_filename = os.path.join(os.path.dirname(__name__), 'advent_of_code', str(year), f'day{day:02d}', "puzzle.txt")
    puzzle = read_file(puzzle_txt_filename).strip("\n")

    module = import_module(f'advent_of_code.{year}.day{day:02d}.part{part}')
    result = module.calculate(puzzle)

    print(f'Result for puzzle {year}-day{day}-part{part} is: {result}')


@click.command()
@click.option('--year', type=int, default=2017)
@click.option('--day', type=int, default=None)
@click.option('--part', type=int, default=None)
def main(year: int, day: Optional[int], part: Optional[int]):
    def run_parts(year: int, day: int):
        if part is None:
            run_puzzle(year, day, part=1)
            run_puzzle(year, day, part=2)
        else:
            run_puzzle(year, day, part=part)

    if day is None:
        # run all the puzzles
        for day in range(1, 25):
            run_parts(year, day)
    else:
        # run the requested puzzle
        run_parts(year, day)


if __name__ == "__main__":
    main()