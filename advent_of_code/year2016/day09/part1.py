import re

RE_MARKER = re.compile('\((\d+)x(\d+)\)')


def calculate(text: str) -> int:
    decompressed = ''
    idx = 0
    while idx < len(text):
        m = RE_MARKER.search(text[idx:])
        if m:
            if m.start() > 0:
                decompressed += text[idx:idx+m.start()]
                idx += m.start()

            input_len = int(m.group(1))
            repeat_count = int(m.group(2))
            idx += m.end() - m.start()

            decompressed += text[idx:idx + input_len] * repeat_count
            idx += input_len
        else:
            decompressed += text[idx:]
            idx = len(text)

    return len(decompressed)


assert calculate("ADVENT") == 6
assert calculate("A(1x5)BC") == 7
assert calculate("(3x3)XYZ") == 9
assert calculate("A(2x2)BCD(2x2)EFG") == 11
assert calculate("(6x1)(1x3)A") == 6
assert calculate("X(8x2)(3x3)ABCY") == 18
