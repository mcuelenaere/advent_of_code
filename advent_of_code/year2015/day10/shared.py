def look_and_say(text: str) -> str:
    i = 0
    out = ""
    while i < len(text):
        char = text[i]
        counter = 1
        while i + 1 < len(text) and text[i + 1] == char:
            counter += 1
            i += 1
        out += f"{counter}{char}"
        i += 1
    return out


assert look_and_say("211") == "1221"
assert look_and_say("1") == "11"
assert look_and_say("11") == "21"
assert look_and_say("21") == "1211"
assert look_and_say("1211") == "111221"
assert look_and_say("111221") == "312211"
