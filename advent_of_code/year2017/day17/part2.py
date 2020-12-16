def calculate(text: str) -> int:
    step_size = int(text)

    position = 0
    val_after_zero = None
    for val in range(1, 50_000_001):
        position += step_size
        position %= val
        if position == 0:
            val_after_zero = val
        position += 1

    return val_after_zero
