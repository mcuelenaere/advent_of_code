from .shared import parse_input, transform


def calculate(text: str) -> int:
    initial_state, transformations = parse_input(text)

    state = initial_state
    min_index = 0
    for i in range(20):
        # make sure we go back early enough
        if not state.startswith("..."):
            state = "..." + state
            min_index -= 3
        # same for at the end
        if not state.endswith("..."):
            state = state + "..."

        state = transform(state, transformations)
    return sum(i + min_index for i, c in enumerate(state) if c == "#")


puzzle = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""".strip()
assert calculate(puzzle) == 325
