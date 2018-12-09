from hashlib import md5


def calculate(text: str) -> str:
    password = ''
    index = 0
    while len(password) < 8:
        digest = ""
        while not digest.startswith("00000"):
            digest = md5(f"{text}{index}".encode()).hexdigest()
            index += 1
        password += digest[5]
    return password


assert calculate("abc") == "18f47a30"
