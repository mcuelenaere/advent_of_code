from .shared import Computer


def calculate(text: str) -> int:
    computers = tuple(Computer(text, i) for i in range(50))

    while any(c.is_running for c in computers):
        for computer in computers:
            for addr, x, y in computer.run_iteration():
                if addr == 255:
                    return y
                computers[addr].queue_packet(x, y)
