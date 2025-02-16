from pathlib import Path
from time import time

YEAR = 2015
DAY = 20
NAME = "Infinite Elves and Infinite Houses"


def part1(input: str) -> int:
    n = int(input.strip())

    counts = [0] * (n // 10)
    for i in range(1, (n // 10) + 1):
        for j in range(i, (n // 10) + 1, i):
            counts[j-1] += i * 10

    for i, count in enumerate(counts, start=1):
        if count > n:
            break

    return i


def part2(input: str) -> int:
    n = int(input.strip())

    counts = [0] * (n // 11)
    for i in range(1, (n // 11) + 1):
        for j in range(i, (n // 11) + 1, i):
            if j <= (i * 50):
                counts[j-1] += i * 11

    for i, count in enumerate(counts, start=1):
        if count > n:
            break

    return i


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day20_full.txt", part1, 665280),
        ("Part 2", "inputs/day20_full.txt", part2, 705600),
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
