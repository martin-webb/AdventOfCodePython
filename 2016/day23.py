from collections.abc import Callable
from pathlib import Path
from time import time

YEAR = 2016
DAY = 23
NAME = "Safe Cracking"

Instruction = Callable[[dict[str, int], list["Instruction"], int], int]


def make_cpy(opl: int | str, opr: str | int) -> Instruction:
    def eval(registers: dict, instructions: list[Instruction], ip: int) -> int:
        # Ordinarily would be a target register (str), but we might have been
        # toggled to an int, in which case skip the instruction
        if isinstance(opr, str):
            value = registers[opl] if opl in registers else int(opl)
            registers[opr] = value
        return 1
    eval.__name__ = "cpy"
    return eval


def make_inc(operand: str) -> Instruction:
    def eval(registers: dict, instructions: list[Instruction], ip: int) -> int:
        registers[operand] += 1
        return 1
    eval.__name__ = "inc"
    return eval


def make_dec(operand: str) -> Instruction:
    def eval(registers: dict, instructions: list[Instruction], ip: int) -> int:
        registers[operand] -= 1
        return 1
    eval.__name__ = "dec"
    return eval


def make_jnz(opl: int | str, opr: int | str) -> Instruction:
    def eval(registers: dict, instructions: list[Instruction], ip: int) -> int:
        # A toggled cpy into jnz can now have registers for either or both
        # operands, so account for this (addition to assembunny from Day 23)
        valueL = registers[opl] if opl in registers else int(opl)
        valueR = registers[opr] if opr in registers else int(opr)
        return valueR if valueL != 0 else 1
    eval.__name__ = "jnz"
    return eval


def make_tgl(_operand: str) -> Instruction:
    def eval(registers: dict, instructions: list[Instruction], ip: int) -> int:
        offset = registers[_operand]

        # If tgl toggles itself
        if offset == 0:
            instructions[ip + offset] = make_inc(_operand)
        elif (ip + offset) < 0 or (ip + offset) >= len(instructions):
            pass
        else:
            instruction_func = instructions[ip + offset]
            kind = instruction_func.__name__
            if kind == "cpy":
                opl = instruction_func.__closure__[0].cell_contents
                opr = instruction_func.__closure__[1].cell_contents
                instructions[ip + offset] = make_jnz(opl, opr)
            elif kind == "inc":
                operand = instruction_func.__closure__[0].cell_contents
                instructions[ip + offset] = make_dec(operand)
            elif kind == "dec":
                operand = instruction_func.__closure__[0].cell_contents
                instructions[ip + offset] = make_inc(operand)
            elif kind == "jnz":
                opl = instruction_func.__closure__[0].cell_contents
                opr = instruction_func.__closure__[1].cell_contents
                instructions[ip + offset] = make_cpy(opl, opr)
            elif kind == "tgl":
                operand = instruction_func.__closure__[0].cell_contents
                instructions[ip + offset] = make_inc(operand)
            else:
                raise RuntimeError(f"Unhandled instruction '{kind}'")
        return 1
    eval.__name__ = "tgl"
    return eval


def parse_input(input: str) -> list[Instruction]:
    """
    Unnecessary closure-based solution to instruction evaluation.
    """
    instructions: list[Instruction] = []

    for line in input.strip().split("\n"):
        parts = line.split()
        if parts[0] == "cpy":
            instruction = make_cpy(parts[1], parts[2])
        elif parts[0] == "inc":
            instruction = make_inc(parts[1])
        elif parts[0] == "dec":
            instruction = make_dec(parts[1])
        elif parts[0] == "jnz":
            instruction = make_jnz(parts[1], parts[2])
        elif parts[0] == "tgl":
            instruction = make_tgl(parts[1])
        else:
            raise RuntimeError(f"Unhandled instruction '{parts[0]}'")

        instructions.append(instruction)

    return instructions


def solve(input: str, registers: dict[str, int]) -> int:
    instructions = parse_input(input)

    ip = 0
    while ip < len(instructions):
        instruction = instructions[ip]
        ip += instruction(registers, instructions, ip)

    result = registers["a"]
    return result


def part1(input: str) -> int:
    registers = dict(a=7, b=0, c=0, d=0)
    result = solve(input, registers)
    return result


def part2(input: str) -> int:
    registers = dict(a=12, b=0, c=0, d=0)
    result = solve(input, registers)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day23_example.txt", part1, 3),
        ("Part 1", "inputs/day23_full.txt", part1, 12775),
        ("Part 1", "inputs/day23_full.txt", part2, 479009335),
    ):
        path = Path(__file__).parent / filename
        with open(path) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)",
              "\u2B50"
              if expected and result == expected and "_full" in filename
              else "")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
