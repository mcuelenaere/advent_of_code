from .shared import parse_password_line


def calculate(text: str):
    valid_passwords = 0
    for line in text.splitlines():
        letter_min, letter_max, letter, password = parse_password_line(line)
        if letter_min <= password.count(letter) <= letter_max:
            valid_passwords += 1
    return valid_passwords


puzzle = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
assert calculate(puzzle) == 2
