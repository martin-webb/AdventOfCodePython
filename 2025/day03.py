from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import Optional

YEAR = 2025
DAY = 3
NAME = "Lobby"


@dataclass
class Found:
    digit: str
    offset: int


def next_digit_from(s: str, n: int, src: int, dst: int) -> Optional[Found]:
    for i, c in enumerate(s[src:dst]):
        if c == str(n):
            return Found(digit=c, offset=i)
    return None


def solve(input: str, n: int) -> int:
    """
    """
    total = 0

    for line in input.strip().split("\n"):
        digits = ""
        src = 0
        for _ in range(n):
            # Searching for the next largest from 9 down to 1
            for m in range(9, 0, -1):
                # We need space for N digits, so limit the space we search in
                # to ensure we can fit the remaining required digit count
                required_space = n - len(digits)
                dst = len(line) - required_space + 1  # OK to go past the end
                result = next_digit_from(line, m, src, dst)
                if result is not None:
                    digits += result.digit
                    src += result.offset + 1
                    break
            else:
                raise RuntimeError(
                    f"Failed to find next digit in: '{line[src:]}'")

        total += int(digits)

    return total


def part1(input: str) -> int:
    return solve(input, 2)


def part2(input: str) -> int:
    return solve(input, 12)


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day03_example.txt", part1, 357),
        ("Part 1", "inputs/day03_full.txt", part1, 17109),
        ("Part 2", "inputs/day03_example.txt", part2, 3121910778619),
        ("Part 2", "inputs/day03_full.txt", part2, 169347417057382),
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
