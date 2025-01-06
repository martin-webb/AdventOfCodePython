from itertools import combinations
from pathlib import Path
from time import time

YEAR = 2023
DAY = 11
NAME = "Cosmic Expansion"


def part1(input: str) -> int:
    lines = input.strip().split("\n")

    galaxies = list()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                galaxies.append((x, y))

    expandable_x = set(range(x + 1))
    expandable_y = set(range(y + 1))

    # Remove any expandable rows and columns. The resulting set indicates which
    # columns are twice as large due to expansion.
    for galaxy in galaxies:
        if galaxy[0] in expandable_x:
            expandable_x.remove(galaxy[0])
        if galaxy[1] in expandable_y:
            expandable_y.remove(galaxy[1])

    expansion_mult = 2
    total_distance = 0

    galaxy_pairs = combinations(galaxies, 2)
    for g1, g2 in galaxy_pairs:
        min_x, max_x = min(g1[0], g2[0]), max(g1[0], g2[0])
        min_y, max_y = min(g1[1], g2[1]), max(g1[1], g2[1])
        xlen = (max_x - min_x) + sum(
            expansion_mult - 1 for n in expandable_x if n > min_x and n < max_x
        )
        ylen = (max_y - min_y) + sum(
            expansion_mult - 1 for n in expandable_y if n > min_y and n < max_y
        )
        distance = xlen + ylen
        total_distance += distance

    return total_distance


def part2(input: str) -> int:
    lines = input.strip().split("\n")

    galaxies = list()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                galaxies.append((x, y))

    expandable_x = set(range(x + 1))
    expandable_y = set(range(y + 1))

    # Remove any expandable rows and columns. The resulting set indicates which
    # columns are twice as large due to expansion.
    for galaxy in galaxies:
        if galaxy[0] in expandable_x:
            expandable_x.remove(galaxy[0])
        if galaxy[1] in expandable_y:
            expandable_y.remove(galaxy[1])

    expansion_mult = 1000000
    total_distance = 0

    galaxy_pairs = combinations(galaxies, 2)
    for g1, g2 in galaxy_pairs:
        min_x, max_x = min(g1[0], g2[0]), max(g1[0], g2[0])
        min_y, max_y = min(g1[1], g2[1]), max(g1[1], g2[1])
        xlen = (max_x - min_x) + sum(
            expansion_mult - 1 for n in expandable_x if n > min_x and n < max_x
        )
        ylen = (max_y - min_y) + sum(
            expansion_mult - 1 for n in expandable_y if n > min_y and n < max_y
        )
        distance = xlen + ylen
        total_distance += distance

    return total_distance


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day11_example.txt", part1, 374),
        ("Part 1", "inputs/day11_full.txt", part1, 9742154),
        ("Part 2", "inputs/day11_example.txt", part2, 82000210),
        ("Part 2", "inputs/day11_full.txt", part2, 411142919886),
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
