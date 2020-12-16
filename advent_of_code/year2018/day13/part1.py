from .shared import advance_carts, find_crashes, parse_track


def calculate(text: str) -> str:
    track = parse_track(text)
    crashes = find_crashes(track)
    while len(crashes) == 0:
        prev_track = track
        track = advance_carts(track)
        crashes = find_crashes(track, prev_track)
    return ",".join(map(str, crashes[0]))


puzzle = r"""
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
""".strip()
assert calculate(puzzle) == "7,3"
