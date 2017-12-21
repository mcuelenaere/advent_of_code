from itertools import chain, product
from typing import Dict, Tuple, Iterator

# NOTE: this could all be implemented so much more succinctly and faster if I had numpy..
PatternMatrix = Tuple[Tuple[bool, ...], ...]


def parse_pattern(text: str) -> PatternMatrix:
    return tuple(tuple(c == '#' for c in line) for line in text.split('/'))


def flip_pattern_horizontally(p: PatternMatrix) -> PatternMatrix:
    return tuple(reversed(p))


def flip_pattern_vertically(p: PatternMatrix) -> PatternMatrix:
    return tuple(tuple(reversed(line)) for line in p)


def rotate_pattern_right(p: PatternMatrix) -> PatternMatrix:
    size = len(p)
    return tuple(tuple(p[y][x] for y in range(size)) for x in range(size - 1, -1, -1))


def parse_pattern_book(text: str) -> Dict[PatternMatrix, PatternMatrix]:
    patterns = {}
    for line in text.splitlines():
        src, dst = line.split(' => ')
        src, dst = parse_pattern(src), parse_pattern(dst)

        # store original pattern
        patterns[src] = dst

        # store flipped patterns
        patterns[flip_pattern_horizontally(src)] = dst
        patterns[flip_pattern_vertically(src)] = dst

        # store rotated (and optionally flipped) patterns
        r = rotate_pattern_right(src)
        patterns[r] = dst
        patterns[flip_pattern_horizontally(r)] = dst
        patterns[flip_pattern_vertically(r)] = dst
        r = rotate_pattern_right(r)
        patterns[r] = dst
        patterns[flip_pattern_horizontally(r)] = dst
        patterns[flip_pattern_vertically(r)] = dst
        r = rotate_pattern_right(r)
        patterns[r] = dst
        patterns[flip_pattern_horizontally(r)] = dst
        patterns[flip_pattern_vertically(r)] = dst

    return patterns


def split_pattern(pattern: PatternMatrix, split_size: int) -> Iterator[PatternMatrix]:
    for y in range(0, len(pattern), split_size):
        for x in range(0, len(pattern), split_size):
            yield tuple(line[x:x+split_size] for line in pattern[y:y+split_size])


def chain_tuple(it):
    return tuple(chain.from_iterable(it))


def merge_patterns(patterns: Tuple[PatternMatrix, ...], stride_size: int) -> PatternMatrix:
    pattern_size = len(patterns[0])
    return tuple(
        chain_tuple(pattern[y] for pattern in patterns[p_y*stride_size:(p_y+1)*stride_size])
        for p_y, y in product(range(stride_size), range(pattern_size))
    )


def process_pattern(pattern: PatternMatrix, book: Dict[PatternMatrix, PatternMatrix]) -> PatternMatrix:
    pattern_size = len(pattern)

    if pattern_size % 2 == 0:
        split_size = 2
    elif pattern_size % 3 == 0:
        split_size = 3
    else:
        raise ValueError()

    subpatterns = tuple(book[subpattern] for subpattern in split_pattern(pattern, split_size))
    return merge_patterns(subpatterns, pattern_size // split_size)


def count_enabled(pattern: PatternMatrix) -> int:
    pattern_size = len(pattern)
    return sum(1 if pattern[x][y] else 0 for x in range(pattern_size) for y in range(pattern_size))
