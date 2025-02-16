from collections.abc import Callable
from pathlib import Path
from time import time

YEAR = 2015
DAY = 23
NAME = "Opening the Turing Lock"


def hlf(op1: str) -> Callable[[dict[str, int]], int]:
    def op(registers: dict[str, int]) -> int:
        registers[op1] //= 2
        return 1
    return op


def tpl(op1: str) -> Callable[[dict[str, int]], int]:
    def op(registers: dict[str, int]) -> int:
        registers[op1] *= 3
        return 1
    return op


def inc(op1: str) -> Callable[[dict[str, int]], int]:
    def op(registers: dict[str, int]) -> int:
        registers[op1] += 1
        return 1
    return op


def jmp(op1: str) -> Callable[[dict[str, int]], int]:
    def op(registers: dict[str, int]) -> int:
        return int(op1)
    return op


def jie(op1: str, op2: str) -> Callable[[dict[str, int]], int]:
    def op(registers: dict[str, int]) -> int:
        return int(op2) if registers[op1] % 2 == 0 else 1
    return op


def jio(op1: str, op2: str) -> Callable[[dict[str, int]], int]:
    def op(registers: dict[str, int]) -> int:
        return int(op2) if registers[op1] == 1 else 1
    return op


def parse_instruction(s: str) -> Callable[[dict[str, int]], int]:
    operator, *operands = s.split()
    if operator == "hlf":
        return hlf(operands[0])
    elif operator == "tpl":
        return tpl(operands[0])
    elif operator == "inc":
        return inc(operands[0])
    elif operator == "jmp":
        return jmp(operands[0])
    elif operator == "jie":
        return jie(operands[0].strip(","), operands[1])
    elif operator == "jio":
        return jio(operands[0].strip(","), operands[1])
    else:
        assert False, "Should not get here"


def parse_input(input: str) -> list[Callable]:
    instructions = [parse_instruction(line)
                    for line in input.strip().split("\n")]
    return instructions


def solve(input: str, a_initial: int, b_initial: int) -> int:
    instructions = parse_input(input)
    registers = dict(a=a_initial, b=b_initial)
    pc = 0
    while True:
        try:
            pc += instructions[pc](registers)
        except IndexError:
            break
    return registers["b"]


def part1(input: str) -> int:
    result = solve(input, 0, 0)
    return result


def part2(input: str) -> int:
    result = solve(input, 1, 0)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day23_full.txt", part1, 184),
        ("Part 2", "inputs/day23_full.txt", part2, 231),
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
