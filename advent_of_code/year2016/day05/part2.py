from hashlib import md5


def calculate(text: str) -> str:
    password = ["_"] * 8
    found = 0
    index = 0
    while found < 8:
        digest = ""
        while not digest.startswith("00000"):
            digest = md5(f"{text}{index}".encode()).hexdigest()
            index += 1

        position = int(digest[5], 16)
        char = digest[6]
        if position > 7 or password[position] != "_":
            # invalid position, skip
            continue

        password[position] = char
        found += 1

    return "".join(password)


assert calculate("abc") == "05ace8e3"
