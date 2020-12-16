from ..day05.shared import streaming_evaluate, parse_instructions


def run_springdroid(intcode_instructions: str, springscript_instructions: str) -> int:
    instructions = parse_instructions(intcode_instructions)
    gen = streaming_evaluate(instructions)

    def expect(expected: str):
        for letter in expected:
            letter = ord(letter)
            actual = next(gen)
            assert actual == letter, f"Got {chr(actual)}, expected {chr(letter)}"

    def send(input: str):
        for letter in input:
            letter = ord(letter)
            res = gen.send(letter)
            assert res is None or res == ord("\n"), f"Expected None or \\n, got {chr(res)}"

    expect("Input instructions:\n")
    gen.send(ord("\n"))
    send(springscript_instructions)
    gen.send(ord("\n"))
    if springscript_instructions.endswith("RUN"):
        expect("Running...\n\n")
    else:
        expect("Walking...\n\n")

    res = next(gen)
    if res < 0xFF:
        # we failed at walking, get the output and throw an error
        buf = [res]
        while True:
            try:
                buf.append(next(gen))
            except StopIteration:
                break
        raise RuntimeError(''.join(chr(c) for c in buf))

    return res
