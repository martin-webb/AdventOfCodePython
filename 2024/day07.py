from math import ceil, log10
from time import time

YEAR = 2024
DAY = 7
NAME = "Bridge Repair"


def solutions(
        target: int, operands: list[int], total: int = 0, i: int = 0) -> int:
    if i < len(operands):
        return (
            solutions(target, operands, total + operands[i], i+1)
            + solutions(target, operands, total * operands[i], i+1)
        )
    else:
        return total == target


def solutions2(
        target: int, operands: list[int], total: int = 0, i: int = 0) -> int:
    if i < len(operands):
        return (
            solutions2(target, operands, total + operands[i], i+1)
            + solutions2(target, operands, total * operands[i], i+1)
            + solutions2(
                target, operands,
                (total * 10**ceil(log10(operands[i]+1))) + operands[i],
                i+1
            )
        )
    else:
        return total == target


def part1(input: str) -> int:
    result = 0

    for line in input.strip().split("\n"):
        total = int(line.split(":")[0])
        operands = [int(n) for n in line.split(":")[1].split()]
        num_solutions = solutions(total, operands)
        if num_solutions > 0:
            result += total

    return result


def part2(input: str) -> int:
    result = 0

    for line in input.strip().split("\n"):
        total = int(line.split(":")[0])
        operands = [int(n) for n in line.split(":")[1].split()]
        num_solutions = solutions2(total, operands)
        if num_solutions > 0:
            result += total

    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day07_example.txt", part1, 3749),
        ("Part 1", "inputs/day07_full.txt", part1, 12553187650171),
        ("Part 2", "inputs/day07_example.txt", part2, 11387),
        ("Part 2", "inputs/day07_full.txt", part2, 96779702119491),
    ):
        with open(filename) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
