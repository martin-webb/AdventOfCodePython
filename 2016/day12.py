from collections.abc import Callable
from pathlib import Path
from time import time

YEAR = 2016
DAY = 12
NAME = "Leonardo's Monorail"


def make_cpy(opl: int | str, opr: str) -> Callable[[dict[str, int]], int]:
    def eval(registers: dict) -> int:
        value = registers[opl] if opl in registers else int(opl)
        registers[opr] = value
        return 1
    return eval


def make_inc(operand: str) -> Callable[[dict[str, int]], int]:
    def eval(registers: dict) -> int:
        registers[operand] += 1
        return 1
    return eval


def make_dec(operand: str) -> Callable[[dict[str, int]], int]:
    def eval(registers: dict) -> int:
        registers[operand] -= 1
        return 1
    return eval


def make_jnz(opl: int | str, opr: int) -> Callable[[dict[str, int]], int]:
    def eval(registers: dict) -> int:
        value = registers[opl] if opl in registers else int(opl)
        return opr if value != 0 else 1
    return eval


def parse_input(input: str) -> list[Callable[[dict[str, int]], int]]:
    """
    Unnecessary closure-based solution to instruction evaluation.
    """
    instructions: list[Callable[[dict[str, int]], int]] = []

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
        instructions.append(instruction)

    return instructions


def solve(input: str, registers: dict[str, int]) -> int:
    instructions = parse_input(input)

    ip = 0
    while ip < len(instructions):
        instruction = instructions[ip]
        ip += instruction(registers)

    result = registers["a"]
    return result


def part1(input: str) -> int:
    registers = dict(a=0, b=0, c=0, d=0)
    result = solve(input, registers)
    return result


def part2(input: str) -> int:
    registers = dict(a=0, b=0, c=1, d=0)
    result = solve(input, registers)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day12_sample.txt", part1, 42),
        ("Part 1", "inputs/day12_full.txt", part1, 318117),
        ("Part 2", "inputs/day12_full.txt", part2, 9227771),
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
