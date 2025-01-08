import re
from pathlib import Path
from time import time

YEAR = 2015
DAY = 5
NAME = "Doesn't He Have Intern-Elves For This?"


def part1(input: str) -> int:
    vowels = re.compile(r"[aeiou]")
    pairs = re.compile(r"(.)\1")
    invalid = re.compile(r"ab|cd|pq|xy")

    return sum([
        1 if len(vowels.findall(s)) >= 3
        and pairs.search(s)
        and invalid.search(s) is None
        else 0
        for s in input.strip().split("\n")
    ])


def part2(input: str) -> int:
    repeated_pairs = re.compile(r"(..).*\1")
    repeats_with_middle = re.compile(r"(.).\1")

    return sum(
        1 if repeated_pairs.findall(s) and repeats_with_middle.search(s) else 0
        for s in input.strip().split("\n")
    )


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day05_full.txt", part1, 258),
        ("Part 2", "inputs/day05_full.txt", part2, 53)
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
