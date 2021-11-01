[![Test puzzles](https://github.com/mcuelenaere/advent_of_code/workflows/Test%20puzzles/badge.svg?branch=master)](https://github.com/mcuelenaere/advent_of_code/actions?query=workflow%3A%22Test+puzzles%22)
# Advent of Code

This is my implementation of the puzzles found at [adventofcode.com](https://adventofcode.com/).

## Getting Started

### Prerequisites

You'll need Python 3 and [poetry](https://python-poetry.org/).

### Installing

The Python dependencies are specified in `pyproject.toml`, install them like this:

```
poetry install
```

### Running the puzzles

There is a CLI runner, which allows you to invoke the code to run a certain puzzle:

```
poetry run solve_puzzle --year 2017 --day 1
```

Or just run them all like this:

```
poetry run solve_puzzle --year 2017
```
