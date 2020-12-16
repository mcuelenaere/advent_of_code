import json


def walk(item) -> int:
    if isinstance(item, int):
        return item
    elif isinstance(item, list):
        return sum(walk(x) for x in item)
    elif isinstance(item, dict):
        if "red" in item.values():
            return 0
        return sum(walk(x) for x in item.values())
    elif isinstance(item, str):
        return 0
    else:
        raise ValueError(f"Unknown type {type(item)}: {item}")


def calculate(text: str) -> int:
    item = json.loads(text)
    return walk(item)


assert calculate("""[1,2,3]""") == 6
assert calculate("""[1,{"c":"red","b":2},3]""") == 4
assert calculate("""{"d":"red","e":[1,2,3,4],"f":5}""") == 0
assert calculate("""[1,"red",5]""") == 6
