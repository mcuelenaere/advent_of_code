from .shared import parse_passports


def calculate(text: str) -> int:
    required_fields = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
    passports = parse_passports(text)
    valid_passwords = 0
    for passport in passports:
        if all(field in passport for field in required_fields):
            valid_passwords += 1
    return valid_passwords


puzzle = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
assert calculate(puzzle) == 2
