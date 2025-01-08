from pathlib import Path
from time import time

YEAR = 2015
DAY = 1
NAME = "Not Quite Lisp"


def part1(input: str) -> int:
    return input.count("(") - input.count(")")


def part2(input: str) -> int:
    floor = 0
    for i, c in enumerate(input, start=1):
        floor += 1 if c == "(" else -1 if c == ")" else 0
        if floor == -1:
            break
    return i


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day01_full.txt", part1, 74),
        ("Part 2", "inputs/day01_full.txt", part2, 1795),
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
