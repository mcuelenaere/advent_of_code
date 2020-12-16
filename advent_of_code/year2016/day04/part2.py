from .shared import Instruction, is_real_room, parse_instructions


def decrypt_name(instruction: Instruction) -> str:
    decrypted = ""
    for letter in instruction.encrypted_name:
        if letter == "-":
            decrypted += " "
        else:
            decrypted += chr((ord(letter) - ord("a") + instruction.sector_id) % 26 + ord("a"))
    return decrypted


assert (
    decrypt_name(Instruction(encrypted_name="qzmt-zixmtkozy-ivhz", sector_id=343, checksum="foobar"))
    == "very encrypted name"
)


def calculate(text: str) -> int:
    for instruction in parse_instructions(text):
        if not is_real_room(instruction):
            continue

        if decrypt_name(instruction) == "northpole object storage":
            return instruction.sector_id
