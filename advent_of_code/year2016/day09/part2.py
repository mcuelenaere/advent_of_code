import re


RE_MARKER = re.compile(r"\((\d+)x(\d+)\)")


def decompressed_size(text: str) -> int:
    length = 0
    idx = 0
    while idx < len(text):
        m = RE_MARKER.search(text[idx:])
        if m:
            if m.start() > 0:
                length += m.start()
                idx += m.start()

            input_len = int(m.group(1))
            repeat_count = int(m.group(2))
            idx += m.end() - m.start()

            length += decompressed_size(text[idx : idx + input_len]) * repeat_count
            idx += input_len
        else:
            length += len(text) - idx
            idx = len(text)
    return length


def calculate(text: str) -> int:
    return decompressed_size(text)


assert calculate("(3x3)XYZ") == 9
assert calculate("X(8x2)(3x3)ABCY") == 20
assert calculate("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920
assert calculate("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445
