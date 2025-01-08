from pathlib import Path
from time import time

YEAR = 2015
DAY = 3
NAME = "Perfectly Spherical Houses in a Vacuum"


def part1(input: str) -> int:
    visited: set[tuple[int, int]] = set()

    x = y = 0
    visited.add((x, y))

    directions = input.strip()
    for direction in directions:
        if direction == "^":
            y -= 1
        elif direction == "v":
            y += 1
        elif direction == "<":
            x -= 1
        elif direction == ">":
            x += 1

        visited.add((x, y))

    return len(visited)


def part2(input: str) -> int:
    visited: set[tuple[int, int]] = set()

    x1 = y1 = x2 = y2 = 0
    visited.add((x1, y1))

    directions = input.strip()
    for d1, d2 in zip(directions[0::2], directions[1::2]):
        if d1 == "^":
            y1 -= 1
        elif d1 == "v":
            y1 += 1
        elif d1 == "<":
            x1 -= 1
        elif d1 == ">":
            x1 += 1

        if d2 == "^":
            y2 -= 1
        elif d2 == "v":
            y2 += 1
        elif d2 == "<":
            x2 -= 1
        elif d2 == ">":
            x2 += 1

        visited.add((x1, y1))
        visited.add((x2, y2))

    return len(visited)


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day03_full.txt", part1, 2572),
        ("Part 2", "inputs/day03_full.txt", part2, 2631)
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
