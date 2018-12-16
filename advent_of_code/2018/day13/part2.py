from .shared import parse_track, advance_carts, find_crashes


def calculate(text: str) -> str:
    track = parse_track(text)
    while len(track.carts) > 1:
        prev_track = track
        track = advance_carts(track)

        # remove crashing carts
        crashes = find_crashes(track, prev_track)
        carts = tuple(c for c in track.carts if (c.x, c.y) not in crashes)
        track = track._replace(carts=carts)

    return f'{track.carts[0].x},{track.carts[0].y}'


puzzle = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
""".strip()
assert calculate(puzzle) == "6,4"
