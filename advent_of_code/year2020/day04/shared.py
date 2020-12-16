from typing import List, Dict


def parse_passports(text: str) -> List[Dict[str, str]]:
    current_items = {}
    passports = []
    for line in text.splitlines():
        if line == "":
            passports.append(current_items)
            current_items = {}
            continue

        for item in line.split(" "):
            key, value = item.split(":", 2)
            current_items[key] = value

    if len(current_items) > 0:
        passports.append(current_items)

    return passports
