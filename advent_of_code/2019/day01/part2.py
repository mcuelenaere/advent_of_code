from math import floor


def calculate(text: str):
    masses = tuple(map(int, text.split()))
    total_fuel_requirement = 0
    for mass in masses:
        fuel = floor(mass / 3) - 2
        fuel_requirement = fuel
        while fuel > 0:
            fuel = floor(fuel / 3) - 2
            if fuel > 0:
                fuel_requirement += fuel

        total_fuel_requirement += fuel_requirement
    return total_fuel_requirement


assert calculate("14\n") == 2
assert calculate("1969\n") == 966
assert calculate("100756\n") == 50346
