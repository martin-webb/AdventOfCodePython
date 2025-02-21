from pathlib import Path
import re
from time import time

YEAR = 2015
DAY = 25
NAME = "Let It Snow"


def parse_input(input: str) -> tuple[int, int]:
    match_row = re.search("row ([0-9]+)", input)
    match_column = re.search("column ([0-9]+)", input)
    assert match_row is not None
    assert match_column is not None
    row = int(match_row.group(1))
    column = int(match_column.group(1))
    return (row, column)


def part1(input: str) -> int:
    row, column = parse_input(input)

    n = sum(range(row + column - 1)) + column

    code = 20151125
    for _ in range(n - 1):
        code = (code * 252533) % 33554393

    return code


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day25_full.txt", part1, 8997277),
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
