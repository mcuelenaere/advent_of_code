from .shared import parse_lines, Circuit, AssignNumber


def calculate(text: str) -> int:
    circuit = Circuit()
    for gate in parse_lines(text.splitlines()):
        circuit.add_gate(gate)

    # do some magic
    a_value = circuit.get_wire_value('a')
    circuit.add_gate(AssignNumber(value=a_value, sink='b'))
    circuit.reset()

    return circuit.get_wire_value('a')
