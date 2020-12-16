from .shared import Circuit, parse_lines


def calculate(text: str) -> int:
    circuit = Circuit()
    for gate in parse_lines(text.splitlines()):
        circuit.add_gate(gate)
    return circuit.get_wire_value("a")


puzzle = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
""".strip()
circuit = Circuit()
for gate in parse_lines(puzzle.splitlines()):
    circuit.add_gate(gate)
assert circuit.get_wire_value("d") == 72
assert circuit.get_wire_value("e") == 507
assert circuit.get_wire_value("f") == 492
assert circuit.get_wire_value("g") == 114
assert circuit.get_wire_value("h") == 65412
assert circuit.get_wire_value("i") == 65079
assert circuit.get_wire_value("x") == 123
assert circuit.get_wire_value("y") == 456
