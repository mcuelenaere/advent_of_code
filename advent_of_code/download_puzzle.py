import os
import re

from datetime import datetime
from time import sleep
from typing import Optional

import click
import html2markdown
import requests


START_YEAR = 2015
END_YEAR = datetime.now().year if datetime.now().month >= 12 else datetime.now().year - 1
PUZZLE_PATH = os.path.join(os.path.dirname(__file__), "..", "puzzles")
RE_PUZZLE_ANSWER = re.compile(r"Your puzzle answer was \<code\>([^<]+)\<\/code\>")
RE_PUZZLE_DESC = re.compile(r"""\<article class="day-desc"\>(.+?)\<\/article\>""", re.MULTILINE | re.DOTALL)


def fetch_puzzle_input(session_cookie: str, year: int, day: int) -> str:
    resp = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": session_cookie})
    # https://www.reddit.com/r/adventofcode/comments/3v64sb/aoc_is_fragile_please_be_gentle/
    sleep(1)
    return resp.text


def fetch_puzzle(session_cookie: str, year: int, day: int) -> str:
    resp = requests.get(f"https://adventofcode.com/{year}/day/{day}", cookies={"session": session_cookie})
    # https://www.reddit.com/r/adventofcode/comments/3v64sb/aoc_is_fragile_please_be_gentle/
    sleep(1)
    return resp.text


def extract_puzzle_answers(puzzle: str) -> list[str]:
    return RE_PUZZLE_ANSWER.findall(puzzle)


def extract_puzzle_description(puzzle: str) -> str:
    descriptions = []
    for html in RE_PUZZLE_DESC.findall(puzzle):
        html = html.replace("""<h2 id="part2">""", "<h2>")
        markdown = html2markdown.convert(html)
        descriptions.append(markdown)
    return "\n\n".join(descriptions)


def write_file(contents: str, filepath: str):
    os.makedirs(os.path.dirname(filepath), mode=0o755, exist_ok=True)
    with open(filepath, "w", encoding="utf8") as f:
        f.write(contents)


@click.command()
@click.option("--session-cookie", type=str, required=True)
@click.option("--year", type=int, required=False)
def main(session_cookie: str, year: Optional[int]):
    if year is not None:
        years = [year]
    else:
        years = range(START_YEAR, END_YEAR + 1)

    now = datetime.now()
    for year in years:
        for day in range(1, 26):
            if now.year == year and day > now.day:
                continue

            path = os.path.join(PUZZLE_PATH, f"year{year}", f"day{day:02d}")

            # check if puzzle input needs to be downloaded
            input_path = os.path.join(path, "input.txt")
            if not os.path.exists(input_path):
                print(f"Downloading puzzle input for {year} day {day}...")
                puzzle_input = fetch_puzzle_input(session_cookie, year, day)

                print(f"Writing puzzle input for {year} day {day}...")
                write_file(puzzle_input, input_path)

            # check if puzzle answers or descriptions needs to be downloaded
            puzzle_parts = [
                os.path.join(path, "puzzle.md"),
                os.path.join(path, "answer-part1.txt"),
            ]
            if day != 25:
                puzzle_parts.append(os.path.join(path, "answer-part2.txt"))

            if any(not os.path.exists(puzzle_part) for puzzle_part in puzzle_parts):
                print(f"Downloading puzzle for {year} day {day}...")
                puzzle = fetch_puzzle(session_cookie, year, day)

                print(f"Writing puzzle description for {year} day {day}...")
                write_file(extract_puzzle_description(puzzle), os.path.join(path, "puzzle.md"))

                for part, answer in enumerate(extract_puzzle_answers(puzzle), start=1):
                    print(f"Writing puzzle answer for {year} day {day} part {part}...")
                    write_file(answer, os.path.join(path, f"answer-part{part}.txt"))

    print("All done!")
