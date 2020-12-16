from typing import Iterator


def to_base26(n: int) -> str:
    if n == 0:
        return "a"
    text = ""
    while n > 0:
        text = chr(ord("a") + n % 26) + text
        n //= 26
    return text


def from_base26(text: str) -> int:
    number = 0
    for char in text:
        number *= 26
        number += ord(char) - ord("a")
    return number


assert to_base26(10) == "k"
assert to_base26(26) == "ba"
assert from_base26("a") == 0
assert from_base26("z") == 25
assert from_base26("ab") == 1
assert from_base26("ba") == 26
assert from_base26(to_base26(115)) == 115
assert to_base26(from_base26("santa")) == "santa"


def create_santa_passwords(start: str = "a") -> Iterator[str]:
    n = from_base26(start)
    while True:
        yield to_base26(n)
        n += 1


def skip_invalid_chars(password: str) -> str:
    for char in ("i", "o", "l"):
        while char in password:
            pos = len(password) - password.index(char)
            n = from_base26(password)
            # increment the password by whatever offset is needed to get it to next letter,
            # while resetting all the ones right from it to 'a'
            # eg: ibd + baa - bd = jaa
            n += 26 ** (pos - 1)
            n -= n % (26 ** (pos - 1))
            password = to_base26(n)
    return password


def is_valid_password(password: str) -> bool:
    has_forbidden_chars = len({"i", "o", "l"} & set(password)) > 0
    if has_forbidden_chars:
        return False

    pair_indexes = set(idx for idx, (a, b) in enumerate(zip(password, password[1:])) if a == b)
    non_overlapping_pairs_count = sum(
        1 for idx in pair_indexes if idx + 1 not in pair_indexes and idx - 1 not in pair_indexes
    )
    if non_overlapping_pairs_count < 2:
        return False

    ascii = tuple(ord(c) for c in password)
    has_increasing_straight = any(True for a, b, c in zip(ascii, ascii[1:], ascii[2:]) if b == a + 1 and c == b + 1)
    if not has_increasing_straight:
        return False

    return True


def find_next_valid_password(password: str) -> str:
    n = from_base26(password) + 1
    while True:
        password = to_base26(n)
        if {"i", "o", "l"} & set(password):
            password = skip_invalid_chars(password)
            n = from_base26(password)

        if is_valid_password(password):
            return password
        n += 1
