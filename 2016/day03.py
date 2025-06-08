from pathlib import Path
from time import time

YEAR = 2016
DAY = 3
NAME = "Squares With Three Sides"


def part1(input: str) -> int:
    possible = 0

    values: list[int] = list()

    for line in input.strip().split("\n"):
        values += [int(n) for n in line.split()]

    for i in range(0, len(values), 3):
        t = values[i:i+3]
        if t[0] + t[1] > t[2] and t[0] + t[2] > t[1] and t[1] + t[2] > t[0]:
            possible += 1

    return possible


def part2(input: str) -> int:
    possible = 0

    column1: list[int] = list()
    column2: list[int] = list()
    column3: list[int] = list()

    for line in input.strip().split("\n"):
        cols = [int(n) for n in line.split()]
        column1.append(cols[0])
        column2.append(cols[1])
        column3.append(cols[2])

    values = column1 + column2 + column3

    for i in range(0, len(values), 3):
        t = values[i:i+3]
        if t[0] + t[1] > t[2] and t[0] + t[2] > t[1] and t[1] + t[2] > t[0]:
            possible += 1

    return possible


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day03_full.txt", part1, 1032),
        ("Part 2", "inputs/day03_full.txt", part2, 1838),
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
