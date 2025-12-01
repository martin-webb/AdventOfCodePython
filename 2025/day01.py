from pathlib import Path
from time import time

YEAR = 2025
DAY = 1
NAME = "Secret Entrance"


def part1(input: str) -> int:
    n = 50
    num_zeroes = 0

    for line in input.strip().split("\n"):
        direction, difference = line[0], int(line[1:])
        if direction == "L":
            n = (n - difference) % 100
        elif direction == "R":
            n = (n + difference) % 100
        else:
            raise RuntimeError(f"Unsupported direction: '{direction}'")

        if n == 0:
            num_zeroes += 1

    return num_zeroes


def part2(input: str) -> int:
    n = 50
    num_zeroes = 0

    for line in input.strip().split("\n"):
        direction, diff = line[0], int(line[1:])
        quotient, remainder = divmod(diff, 100)

        num_zeroes += quotient

        m = n
        if direction == "L":
            if remainder > 0:
                n -= remainder
                if n <= 0 and m != 0:
                    num_zeroes += 1
                n %= 100

        elif direction == "R":
            if remainder > 0:
                n += remainder
                if n >= 100 and m != 0:
                    num_zeroes += 1
                n %= 100
        else:
            raise RuntimeError(f"Unsupported direction: '{direction}'")

    return num_zeroes


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day01_example.txt", part1, 3),
        ("Part 1", "inputs/day01_full.txt", part1, 1007),
        ("Part 2", "inputs/day01_example.txt", part2, 6),
        ("Part 2", "inputs/day01_full.txt", part2, 5820),
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
