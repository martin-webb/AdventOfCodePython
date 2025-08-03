from pathlib import Path
from time import time

YEAR = 2016
DAY = 15
NAME = "Timing is Everything"


def product(values: list[int]) -> int:
    """
    Like sum() but for multiplication. Not tested with floats.

    >>> product([0,1,2])
    0
    >>> product([1,2,3])
    6
    """
    if len(values) == 1:
        return values[0]
    else:
        return values[0] * product(values[1:])


def parse_input(input: str) -> list[tuple[int, int]]:
    discs = []

    for line in input.strip().split("\n"):
        parts = line.split()
        disc_num = int(parts[1].strip("#"))
        positions = int(parts[3])
        position_at_t0 = int(parts[11].strip("."))
        disc = (((position_at_t0 + disc_num) % positions), positions)
        discs.append(disc)

    return discs


def solve(discs: list[tuple[int, int]]) -> int:
    """
    Simple iterative search (over use of the Chinese Remainder Theorem).
    """
    i = 0
    while True:
        for disc in discs:
            if (disc[0] + i) % disc[1] != 0:
                break
        else:
            break
        i += 1
    return i


def part1(input: str) -> int:
    discs = parse_input(input)
    result = solve(discs)
    return result


def part2(input: str) -> int:
    discs = parse_input(input)
    discs.append(((0 + (len(discs) + 1)) % 11, 11))
    result = solve(discs)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day15_example.txt", part1, 5),
        ("Part 1", "inputs/day15_full.txt", part1, 16824),
        ("Part 2", "inputs/day15_full.txt", part2, 3543984),
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
