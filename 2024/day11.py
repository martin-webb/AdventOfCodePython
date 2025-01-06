from functools import cache
from math import ceil, floor, log10
from pathlib import Path
from time import time

YEAR = 2024
DAY = 11
NAME = "Plutonian Pebbles"


@cache
def num_stones(n: int, iters: int, i: int = 0) -> int:
    if i < iters:
        if n == 0:
            return num_stones(1, iters, i+1)
        elif (num_digits := ceil(log10(n+1))) % 2 == 0:
            left = floor(n / (10 ** (num_digits/2)))
            right = round(n % (10 ** (num_digits/2)))
            return num_stones(left, iters, i+1) + num_stones(right, iters, i+1)
        else:
            return num_stones(n * 2024, iters, i+1)
    else:
        return 1


def part1(input: str) -> int:
    stones: list[int] = list()

    for s in input.strip().split():
        stones.append(int(s))

    count = sum(num_stones(n, 25) for n in stones)
    return count


def part2(input: str) -> int:
    stones: list[int] = list()

    for s in input.strip().split():
        stones.append(int(s))

    count = sum(num_stones(n, 75) for n in stones)
    return count


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day11_example.txt", part1, 55312),
        ("Part 1", "inputs/day11_full.txt", part1, 228668),
        ("Part 2", "inputs/day11_full.txt", part2, 270673834779359),
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
