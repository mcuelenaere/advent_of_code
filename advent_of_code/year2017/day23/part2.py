def decompiled_code():
    # What the puzzle looks like, if you'd decompile it into Python
    h = 0
    for b in range(109_300, 126_300 + 1, 17):
        f = 1
        for d in range(2, b + 1):
            for e in range(2, b + 1):
                if d * e == b:
                    f = 0

        if f == 0:
            h += 1
    return h


def simplified_code():
    # What an optimized version of the puzzle looks like, in Python
    h = 0
    for b in range(109_300, 126_300 + 1, 17):
        f = 1
        d = 2
        while d * d <= b:
            if b % d == 0:
                f = 0
            d += 1

        if f == 0:
            h += 1
    return h


def calculate(_: str) -> int:
    return simplified_code()
