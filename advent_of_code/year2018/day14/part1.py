def calculate(text: str) -> str:
    required_recipe_count = int(text)
    scoreboard = [3, 7]
    elf_indexes = (0, 1)
    for _ in range(required_recipe_count - 2 + 10):
        recipes = str(sum(scoreboard[i] for i in elf_indexes))
        for recipe in recipes:
            scoreboard.append(int(recipe))
        elf_indexes = tuple((i + 1 + scoreboard[i]) % len(scoreboard) for i in elf_indexes)
    return "".join(map(str, scoreboard[required_recipe_count : required_recipe_count + 10]))


assert calculate("9") == "5158916779"
assert calculate("5") == "0124515891"
assert calculate("18") == "9251071085"
assert calculate("2018") == "5941429882"
