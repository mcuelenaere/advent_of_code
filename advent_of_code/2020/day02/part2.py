from .shared import parse_password_line


def calculate(text: str):
    valid_passwords = 0
    for line in text.splitlines():
        letter_pos_1, letter_pos_2, letter, password = parse_password_line(line)
        if (password[letter_pos_1 - 1] == letter) != (password[letter_pos_2 - 1] == letter):
            valid_passwords += 1
    return valid_passwords


puzzle = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
assert calculate(puzzle) == 1
