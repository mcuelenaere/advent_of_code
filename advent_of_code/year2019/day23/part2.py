from .shared import Computer


def calculate(text: str) -> int:
    computers = tuple(Computer(text, i) for i in range(50))
    nat_last_packet = None
    nat_last_y_sent = None

    while any(c.is_running for c in computers):
        for computer in computers:
            message_sent = False
            for addr, x, y in computer.run_iteration():
                message_sent = True
                if addr == 255:
                    nat_last_packet = (x, y)
                else:
                    computers[addr].queue_packet(x, y)

            network_is_idle = (sum(c.queue_length() for c in computers) == 0) and not message_sent
            if network_is_idle and nat_last_packet is not None:
                if nat_last_y_sent == nat_last_packet[1]:
                    return nat_last_packet[1]
                computers[0].queue_packet(nat_last_packet[0], nat_last_packet[1])
                nat_last_y_sent = nat_last_packet[1]
