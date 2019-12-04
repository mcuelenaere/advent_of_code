def validate_password(password: str) -> bool:
    has_double_digits = False
    digits = tuple(map(int, password))
    for prev, cur in zip(digits, digits[1:]):
        if prev == cur:
            has_double_digits = True
        elif prev > cur:
            # can't have decreasing numbers
            return False

    return has_double_digits


assert validate_password("111111")
assert not validate_password("223450")
assert not validate_password("123789")


def calculate(text: str) -> int:
    start, stop = map(int, text.split('-'))
    return sum(1 for password in range(start, stop) if validate_password(str(password)))
