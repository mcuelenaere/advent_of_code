from collections import defaultdict
from enum import Enum
from itertools import chain
from typing import NamedTuple, Dict, Tuple, Optional, List


class CardinalDirection(Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'


Cart = NamedTuple('Cart', x=int, y=int, orientation=CardinalDirection, intersection_count=int)
Track = NamedTuple('Track', track_pieces=Dict[Tuple[int, int], str], carts=Tuple[Cart])

CART_MAPPING = {
    '^': CardinalDirection.NORTH,
    'v': CardinalDirection.SOUTH,
    '<': CardinalDirection.WEST,
    '>': CardinalDirection.EAST,
}


def parse_track(text: str) -> Track:
    cart_to_track = {
        '^': '|',
        'v': '|',
        '<': '-',
        '>': '-',
    }
    carts = list()
    track_pieces = {}
    lines = text.splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == " ":
                continue
            elif c in CART_MAPPING:
                carts.append(Cart(x=x, y=y, orientation=CART_MAPPING[c], intersection_count=0))
                track_pieces[(x, y)] = cart_to_track[c]
            else:
                track_pieces[(x, y)] = c

    return Track(track_pieces=track_pieces, carts=tuple(carts))


CARDINAL_DIRECTION_TO_RELATIVE_COORDINATE = {
    CardinalDirection.NORTH: (0, -1),
    CardinalDirection.EAST: (1, 0),
    CardinalDirection.SOUTH: (0, 1),
    CardinalDirection.WEST: (-1, 0)
}

CURVE_DIRECTION_MAPPING = {
    ('/', CardinalDirection.NORTH): CardinalDirection.EAST,
    ('/', CardinalDirection.EAST): CardinalDirection.NORTH,
    ('/', CardinalDirection.SOUTH): CardinalDirection.WEST,
    ('/', CardinalDirection.WEST): CardinalDirection.SOUTH,
    ('\\', CardinalDirection.NORTH): CardinalDirection.WEST,
    ('\\', CardinalDirection.EAST): CardinalDirection.SOUTH,
    ('\\', CardinalDirection.SOUTH): CardinalDirection.EAST,
    ('\\', CardinalDirection.WEST): CardinalDirection.NORTH,
}


def advance_carts(track: Track) -> Track:
    cardinal_directions = tuple(CardinalDirection.__members__.values())
    new_carts = []
    for cart in track.carts:
        offset = CARDINAL_DIRECTION_TO_RELATIVE_COORDINATE[cart.orientation]
        coordinate = (cart.x + offset[0], cart.y + offset[1])

        # what's at this new coordinate?
        assert coordinate in track.track_pieces
        track_piece = track.track_pieces[coordinate]

        orientation = cart.orientation
        intersection_count = cart.intersection_count
        if track_piece == '+':
            intersection_count += 1
            c = intersection_count % 3
            if c == 1:
                # go left
                orientation = cardinal_directions[(cardinal_directions.index(orientation) - 1) % len(cardinal_directions)]
            elif c == 2:
                # go straight
                pass
            else:
                # go right
                orientation = cardinal_directions[(cardinal_directions.index(orientation) + 1) % len(cardinal_directions)]
        elif track_piece in ('/', '\\'):
            orientation = CURVE_DIRECTION_MAPPING[(track_piece, orientation)]
        elif track_piece in ('|', '-'):
            # don't do anything, straight paths don't change orientation
            pass
        else:
            raise RuntimeError('unknown track piece')

        new_carts.append(Cart(
            x=coordinate[0],
            y=coordinate[1],
            orientation=orientation,
            intersection_count=intersection_count
        ))
    return track._replace(carts=tuple(new_carts))


def find_crashes(track: Track, prev_track: Optional[Track] = None) -> List[Tuple[int, int]]:
    seen_coordinates = set()
    crashes = []
    for cart in chain(prev_track.carts if prev_track else [], track.carts):
        coordinate = (cart.x, cart.y)
        if coordinate in seen_coordinates:
            crashes.append(coordinate)
        seen_coordinates.add(coordinate)
    return crashes


def print_track(track: Track):
    track_pieces = defaultdict(lambda: ' ')
    track_pieces.update(track.track_pieces)

    for cart in track.carts:
        track_pieces[(cart.x, cart.y)] = next(c for c, o in CART_MAPPING.items() if o == cart.orientation)

    max_x = max(x for x, _ in track.track_pieces.keys())
    max_y = max(y for _, y in track.track_pieces.keys())

    for y in range(0, max_y + 1):
        print(''.join(track_pieces[(x, y)] for x in range(0, max_x + 1)))
