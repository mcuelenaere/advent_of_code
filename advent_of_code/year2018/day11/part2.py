from .shared import generate_grid


def calculate(text: str) -> str:
    grid_serial_number = int(text)
    grid = generate_grid(grid_serial_number)

    # calculate rolling sum grid
    rolling_sum_grid = {}
    for y in range(1, 301):
        rolling_sum = 0
        for x in range(1, 301):
            rolling_sum += grid[(x, y)]
            rolling_sum_grid[(1, y, x)] = rolling_sum

        for x in range(2, 301):
            for j in range(1, 301 - x):
                rolling_sum_grid[(x, y, j)] = rolling_sum_grid[(x - 1, y, j + 1)] - grid[(x - 1, y)]

    max_power_level = 0
    best_square = None
    for square_size in range(1, 300):
        for x in range(1, 300 - square_size + 1):
            total_power_level = sum(rolling_sum_grid[(x, 1 + i, square_size)] for i in range(square_size))
            for y in range(1, 300 - square_size + 1):
                if y > 1:
                    total_power_level -= rolling_sum_grid[(x, y - 1, square_size)]
                    total_power_level += rolling_sum_grid[(x, y + square_size - 1, square_size)]

                if total_power_level > max_power_level:
                    max_power_level = total_power_level
                    best_square = f"{x},{y},{square_size}"

    return best_square


assert calculate("18") == "90,269,16"
assert calculate("42") == "232,251,12"
