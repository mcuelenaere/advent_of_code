def parse_schedule(text: str):
    estimate, bus_lines = text.splitlines()
    bus_lines = tuple(int(line) if line != "x" else None for line in bus_lines.split(","))
    return int(estimate), bus_lines
