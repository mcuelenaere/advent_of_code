def calculate(text: str) -> int:
    score = list(map(int, text))
    scoreboard = [3, 7]
    elf1 = 0
    elf2 = 1
    while scoreboard[-len(score):] != score and scoreboard[-len(score)-1:-1] != score:
        total = scoreboard[elf1] + scoreboard[elf2]
        if total >= 10:
            scoreboard.extend(divmod(total, 10))
        else:
            scoreboard.append(total)
        elf1 = (elf1 + 1 + scoreboard[elf1]) % len(scoreboard)
        elf2 = (elf2 + 1 + scoreboard[elf2]) % len(scoreboard)
    return len(scoreboard) - len(text) - (0 if scoreboard[-len(score):] == score else 1)


assert calculate("51589") == 9
assert calculate("01245") == 5
assert calculate("92510") == 18
assert calculate("59414") == 2018
