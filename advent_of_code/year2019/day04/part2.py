def validate_password(password: str) -> bool:
    has_double_digits = False
    multi_digits_counter = 0
    digits = tuple(map(int, password))
    for prev, cur in zip(digits, digits[1:]):
        if prev > cur:
            # can't have decreasing numbers
            return False
        elif prev == cur:
            # keep track of how many times we saw this digit
            multi_digits_counter += 1
        else:
            if multi_digits_counter == 1:
                # the repeating digit has been seen exactly 2 times
                has_double_digits = True

            # reset counter
            multi_digits_counter = 0

    if multi_digits_counter == 1:
        # the repeating digit has been seen exactly 2 times
        has_double_digits = True

    return has_double_digits


assert validate_password("112233")
assert not validate_password("123444")
assert validate_password("111122")


def calculate(text: str) -> int:
    start, stop = map(int, text.split('-'))
    return sum(1 for password in range(start, stop) if validate_password(str(password)))
