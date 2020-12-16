import re

POLYMER_BASE_UNITS = tuple("abcdefghijklmnopqrstuvwxyz")

# construct regex matching units of opposite polymers
RE_POLYMER_OPPOSITE_UNITS = re.compile("|".join(f"{l}{l.upper()}|{l.upper()}{l}" for l in POLYMER_BASE_UNITS))


def react_polymer(text: str) -> str:
    # keep replacing units until nothing changes anymore
    did_react = True
    while did_react:
        old_len = len(text)
        text = RE_POLYMER_OPPOSITE_UNITS.sub('', text)
        new_len = len(text)
        did_react = new_len != old_len

    return text
