from typing import Iterable


def calculate_presents_for_house(house_number: int) -> int:
    presents = 0
    for elf in range(1, house_number + 1):
        if house_number % elf == 0:
            presents += elf * 10
    return presents


def houses(start_number: int = 1) -> Iterable[int]:
    house = start_number
    while True:
        presents = calculate_presents_for_house(house)
        yield (house, presents)
        house += 1


def bruteforce_search(min_number_of_presents: int) -> int:
    for house_number, number_of_presents in houses():
        if house_number > 100:
            raise RuntimeError()
        if number_of_presents >= min_number_of_presents:
            return house_number


def binary_search(min_number_of_presents: int) -> int:
    # first, find *a* house that has more presents
    upper_bound = 1
    while calculate_presents_for_house(upper_bound) < min_number_of_presents:
        upper_bound *= 2

    lower_bound = upper_bound // 2
    for house_number, number_of_presents in houses(lower_bound):
        if number_of_presents >= min_number_of_presents:
            print('found', house_number)
            return house_number
    print(upper_bound, lower_bound)


def calculate(text: str) -> int:
    min_number_of_presents = int(text)
    binary_search(min_number_of_presents)
    return bruteforce_search(min_number_of_presents)


assert calculate("10") == 1
assert calculate("30") == 2
assert calculate("40") == 3
assert calculate("70") == 4
assert calculate("120") == 6
assert calculate("150") == 8
