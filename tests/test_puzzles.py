import os
import re

from glob import iglob
from importlib import import_module

import pytest


PUZZLE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "puzzles"))


def read_file(filename: str) -> str:
    with open(filename, mode="r") as f:
        return f.read()


def list_all_puzzle_answers():
    re_year = re.compile(r"year(\d+)")
    re_day = re.compile(r"day(\d+)")
    re_part = re.compile(r"answer-part([12]).txt")

    for answer in iglob(os.path.join(PUZZLE_PATH, "**", "answer-part?.txt"), recursive=True):
        path_parts = os.path.relpath(answer, PUZZLE_PATH).split(os.sep)
        year = int(re_year.match(path_parts[0]).group(1))
        day = int(re_day.match(path_parts[1]).group(1))
        part = int(re_part.match(path_parts[2]).group(1))
        yield year, day, part


@pytest.mark.parametrize("year,day,part", list_all_puzzle_answers())
def test_correctly_solve_puzzle(year: int, day: int, part: int):
    puzzle_input = read_file(os.path.join(PUZZLE_PATH, f"year{year}", f"day{day:02d}", "input.txt")).strip("\n")
    expected_answer = read_file(os.path.join(PUZZLE_PATH, f"year{year}", f"day{day:02d}", f"answer-part{part}.txt"))

    module = import_module(f"advent_of_code.year{year}.day{day:02d}.part{part}")
    actual_answer = module.calculate(puzzle_input)

    # coerce expected answer to correct type, if needed
    if type(actual_answer) != str:
        expected_answer = (type(actual_answer))(expected_answer)

    assert actual_answer == expected_answer
