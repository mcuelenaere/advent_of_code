import re

from .shared import parse_passports


def calculate(text: str) -> int:
    required_fields = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
    passports = parse_passports(text)
    valid_passwords = 0
    for passport in passports:
        if not all(field in passport for field in required_fields):
            continue

        is_valid = True
        for field, value in passport.items():
            try:
                if field == "byr":
                    assert len(value) == 4
                    assert 1920 <= int(value) <= 2002
                elif field == "iyr":
                    assert len(value) == 4
                    assert 2010 <= int(value) <= 2020
                elif field == "eyr":
                    assert len(value) == 4
                    assert 2020 <= int(value) <= 2030
                elif field == "hgt":
                    assert value.endswith("cm") or value.endswith("in")
                    if value.endswith("cm"):
                        assert 150 <= int(value[:-2]) <= 193
                    else:
                        assert 59 <= int(value[:-2]) <= 76
                elif field == "hcl":
                    assert re.match(r"^#[0-9a-f]{6}$", value) is not None
                elif field == "ecl":
                    assert value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
                elif field == "pid":
                    assert len(value) == 9
                    assert int(value)
            except AssertionError:
                is_valid = False
                break

        if is_valid:
            valid_passwords += 1
    return valid_passwords


puzzle = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""
assert calculate(puzzle) == 0
puzzle = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""
assert calculate(puzzle) == 4
