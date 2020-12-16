from .shared import parse_input, transform


def calculate(text: str) -> int:
    initial_state, transformations = parse_input(text)

    state = initial_state
    min_index = 0

    # make sure we go back early enough
    if not state.startswith("..."):
        state = "..." + state
        min_index -= 3
    # same for at the end
    if not state.endswith("..."):
        state = state + "..."

    # keep transforming until we're out of possibilities
    for i in range(200):
        state = transform(state, transformations) + "."

    # after this, nothing seems to be happening except that it moves to the right
    return sum(i + min_index + 50000000000 - 200 for i, c in enumerate(state) if c == "#")
