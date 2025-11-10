from collections.abc import Callable
from pathlib import Path
from time import time

YEAR = 2016
DAY = 25
NAME = "Clock Signal"

Instruction = Callable[[dict[str, int], list[int]], int]


def make_cpy(opl: int | str, opr: str) -> Instruction:
    def eval(registers: dict, output: list[int]) -> int:
        value = registers[opl] if opl in registers else int(opl)
        registers[opr] = value
        return 1
    return eval


def make_inc(operand: str) -> Instruction:
    def eval(registers: dict, output: list[int]) -> int:
        registers[operand] += 1
        return 1
    return eval


def make_dec(operand: str) -> Instruction:
    def eval(registers: dict, output: list[int]) -> int:
        registers[operand] -= 1
        return 1
    return eval


def make_jnz(opl: int | str, opr: int) -> Instruction:
    def eval(registers: dict, output: list[int]) -> int:
        value = registers[opl] if opl in registers else int(opl)
        return opr if value != 0 else 1
    return eval


def make_out(operand: str) -> Instruction:
    def eval(registers: dict, output: list[int]) -> int:
        value = registers[operand]
        output.append(value)
        return 1
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
            instruction = make_jnz(parts[1], int(parts[2]))
        elif parts[0] == "out":
            instruction = make_out(parts[1])
        else:
            raise RuntimeError(f"Unhandled instruction '{parts[0]}'")

        instructions.append(instruction)

    return instructions


def run_until_n_outputs(
        instructions: list[Instruction],
        registers: dict[str, int],
        num_outputs: int
        ) -> list[int]:
    output: list[int] = []

    ip = 0
    while ip < len(instructions):
        instruction = instructions[ip]
        ip += instruction(registers, output)
        if len(output) == num_outputs:
            break

    return output


def part1(input: str) -> int:
    """
    Simplest approach, let's just test incrementing values of a and check the
    outputs for a periodic signal, running the program until we have N outputs.
    """
    instructions = parse_input(input)

    # Minimum required size to find the periodic signal for our input (found by
    # manual testing and saved here).
    # NOTE: The puzzle description lists 10 integers as its example which might
    # be a hint but might not. It seems like we can get away with fewer though.
    num_outputs = 8

    n = 0
    while True:
        registers = dict(a=n, b=0, c=0, d=0)
        result = run_until_n_outputs(instructions, registers, num_outputs)
        expected = [0, 1] * (num_outputs // 2)
        if result == expected:
            break
        n += 1

    return n


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day25_full.txt", part1, 196),
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
