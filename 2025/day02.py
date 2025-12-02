from math import ceil, log10
from pathlib import Path
import re
from time import time

YEAR = 2025
DAY = 2
NAME = "Gift Shop"


def part1(input: str) -> int:
    total = 0

    ranges = input.strip().split(",")
    for r in ranges:
        begin, end = [int(n) for n in r.split("-")]
        for n in range(begin, end+1):
            num_digits = ceil(log10(n+1))
            match_length = ceil(num_digits / 2)
            pattern = rf"([0-9]{{{match_length}}})\1"
            match = re.match(pattern, str(n))
            if match is not None:
                total += n

    return total


def part2(input: str) -> int:
    total = 0

    ranges = input.strip().split(",")
    for r in ranges:
        begin, end = [int(n) for n in r.split("-")]
        for n in range(begin, end+1):
            num_digits = ceil(log10(n+1))
            max_match_length = ceil(num_digits / 2)
            for l in range(1, max_match_length+1):
                pattern = rf"^([0-9]{{{l}}})\1+$"
                match = re.match(pattern, str(n))
                if match is not None:
                    total += n
                    break

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day02_example.txt", part1, 1227775554),
        ("Part 1", "inputs/day02_full.txt", part1, 64215794229),
        ("Part 2", "inputs/day02_example.txt", part2, 4174379265),
        ("Part 2", "inputs/day02_full.txt", part2, 85513235135),
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
