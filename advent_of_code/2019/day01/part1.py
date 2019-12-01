from math import floor


def calculate(text: str):
    masses = map(int, text.split())
    total_fuel_requirement = 0
    for mass in masses:
        fuel_requirement = floor(mass / 3) - 2
        total_fuel_requirement += fuel_requirement
    return total_fuel_requirement


assert calculate("12\n") == 2
assert calculate("14\n") == 2
assert calculate("1969\n") == 654
assert calculate("100756\n") == 33583
