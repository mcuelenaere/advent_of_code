[![Test puzzles](https://github.com/mcuelenaere/advent_of_code/actions/workflows/run_tests.yml/badge.svg?branch=master)](https://github.com/mcuelenaere/advent_of_code/actions/workflows/run_tests.yml)
[![Code quality](https://github.com/mcuelenaere/advent_of_code/actions/workflows/code-quality.yml/badge.svg?branch=master)](https://github.com/mcuelenaere/advent_of_code/actions/workflows/code-quality.yml)

# Advent of Code

This is my implementation of the puzzles found at [adventofcode.com](https://adventofcode.com/).

## Personal goals

### 2017

No explicit goal.

### 2018

No explicit goal.

### 2019

No explicit goal.

### 2020

> Goal: all solutions must be solved in under 1 second.

This sometimes resulted in resorting to C++ for certain puzzles, so the solutions aren't 100% in Python anymore.

### 2021

> Goal: all solutions must be written in Rust.

This means that all solutions written since 2021 are in Rust (so not just all puzzles from 2021, but also some of the older years that were solved in 2021).

## Getting Started

### Prerequisites

You'll need Python 3, [poetry](https://python-poetry.org/) and Rust.

### Installing

The Python dependencies are specified in `pyproject.toml`, install them like this:

```bash
poetry install
```

The Rust dependencies are specified in `rust/Cargo.toml`, they are installed automatically if you run the above command.

### Solving the puzzles

The following command allows you to solve a certain puzzle:

```bash
poetry run solve_puzzle --year 2017 --day 1
```

Or just solve all puzzles of that year:

```bash
poetry run solve_puzzle --year 2017
```

Or solve all puzzles:

```bash
poetry run solve_puzzle
```

### Downloading new puzzles

If new puzzles are released, they can be downloaded using the following command:

```bash
poetry run download_puzzle --session-cookie="..." --year 2021
```

The session cookie refers to the `session` HTTP cookie being set on [adventofcode.com](https://adventofcode.com/).
