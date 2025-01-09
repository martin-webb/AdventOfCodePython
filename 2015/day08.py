from pathlib import Path
import re
from time import time

YEAR = 2015
DAY = 8
NAME = "Matchsticks"


def part1(input: str) -> int:
    result = 0

    for line in input.strip().split("\n"):
        # NOTE: We don't actually need to replace with the character as we just
        # need the length of the string, so just replace with a space. This
        # also accounts for both the \\ and \" single character replacements
        # and the \xXX hex replacements.
        unencoded = re.sub(r'\\(\\|"|x[0-9a-fA-F]{2})', ' ', line)
        unencoded_length = len(unencoded) - 2
        result += len(line) - unencoded_length

    return result


def part2(input: str) -> int:
    result = 0

    for line in input.strip().split("\n"):
        encoded = re.sub(r'("|\\)', '\\\1', line)
        encoded_length = len(encoded) + 2
        result += encoded_length - len(line)

    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day08_example.txt", part1, 12),
        ("Part 1", "inputs/day08_full.txt", part1, 1333),
        ("Part 2", "inputs/day08_example.txt", part2, 19),
        ("Part 2", "inputs/day08_full.txt", part2, 2046)
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
