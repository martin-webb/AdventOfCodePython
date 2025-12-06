from pathlib import Path
from time import time
from typing import Callable

YEAR = 2025
DAY = 6
NAME = "Trash Compactor"

OpFunc = Callable[[int, int], int]


def parse_operators_line(line: str) -> tuple[list[int], list[OpFunc]]:
    """
    Parse the final line into two lists, one containing running subtotals and
    the other containing lambda expressions that can be applied to a subtotal
    and an operand.
    """
    subtotals: list[int] = list()
    operators: list[OpFunc] = list()

    for operator in line.split():
        if operator == "+":
            subtotals.append(0)
            operators.append(lambda total, n: total + n)
        elif operator == "*":
            subtotals.append(1)
            operators.append(lambda total, n: total * n)
        else:
            assert False, f"Unsupported operator '{operator}'"

    return (subtotals, operators)


def transpose_operands_lines(lines: list[str]) -> list[str]:
    """
    Part 2 input transformer to transpose the row-based input into columns.
    """
    transposed = []

    grid: list[list[str]] = list()
    for line in lines:
        grid.append(list(line))

    for x in range(len(grid[0]) - 1, -1, -1):
        s = ""
        for y in range(len(grid)):
            s += grid[y][x]
        transposed.append(s)

    return transposed


def part1(input: str) -> int:
    lines = input.strip().split("\n")

    operand_lines = lines[:-1]
    operator_line = lines[-1]

    # Operator parsing can be the same for parts 1 and 2
    subtotals, operators = parse_operators_line(operator_line)

    # Cephalopod math
    for line in reversed(operand_lines):
        operands = line.split()
        for x, operand in enumerate(operands):
            subtotals[x] = operators[x](subtotals[x], int(operand))

    total = sum(subtotals)
    return total


def part2(input: str) -> int:
    lines = input.strip().split("\n")

    operand_lines = lines[:-1]
    operator_line = lines[-1]

    # Operator parsing can be the same for parts 1 and 2
    subtotals, operators = parse_operators_line(operator_line)

    # Cephalopod math
    columns = transpose_operands_lines(operand_lines)

    x = len(subtotals) - 1
    for operand in columns:
        if operand.isspace():
            x -= 1
        else:
            subtotals[x] = operators[x](subtotals[x], int(operand))

    total = sum(subtotals)
    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day06_example.txt", part1, 4277556),
        ("Part 1", "inputs/day06_full.txt", part1, 5316572080628),
        ("Part 2", "inputs/day06_example.txt", part2, 3263827),
        ("Part 2", "inputs/day06_full.txt", part2, 11299263623062),
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
