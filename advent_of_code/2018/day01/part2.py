def calculate(text: str) -> int:
    seen_frequencies = set()
    change_set = text.splitlines()

    current_frequency = 0
    while True:
        for freq_change in change_set:
            current_frequency += int(freq_change)
            if current_frequency in seen_frequencies:
                # first time we've seen a frequency happen twice
                return current_frequency
            seen_frequencies.add(current_frequency)


puzzle = """
+1
-2
+3
+1
""".strip()
assert calculate(puzzle) == 2
