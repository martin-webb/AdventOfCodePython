from collections import Counter
from pathlib import Path
from time import time

YEAR = 2024
DAY = 1
NAME = "Historian Hysteria"


def part1(input: str) -> int:
    left = []
    right = []

    for line in input.strip().split("\n"):
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))

    total = 0
    for l, r in zip(sorted(left), sorted(right)):
        total += abs(l - r)

    return total


def part2(input: str) -> int:
    left = []
    right = []

    for line in input.strip().split("\n"):
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))

    right_count = Counter(right)

    total = 0
    for l in left:
        total += l * right_count[l]

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day01_example.txt", part1, 11),
        ("Part 1", "inputs/day01_full.txt", part1, 1151792),
        ("Part 2", "inputs/day01_example.txt", part2, 31),
        ("Part 2", "inputs/day01_full.txt", part2, 21790168),
    ):
        path = Path(__file__).parent / filename
        with open(path) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
