import json
from pathlib import Path
from time import time
from typing import Optional, Union

YEAR = 2015
DAY = 12
NAME = "JSAbacusFramework.io"


def sum_numbers(
    value: Union[str | int | list | dict],
    ignore: Optional[str] = None,
) -> int:
    total = 0

    if isinstance(value, list):
        for v in value:
            total += sum_numbers(v, ignore)

    elif isinstance(value, dict):
        if ignore not in value.values():
            for v in value.values():
                total += sum_numbers(v, ignore)

    elif isinstance(value, int):
        total += value

    return total


def part1(input: str) -> int:
    data = json.loads(input)
    total = sum_numbers(data)
    return total


def part2(input: str) -> int:
    data = json.loads(input)
    total = sum_numbers(data, "red")
    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day12_full.txt", part1, 111754),
        ("Part 2", "inputs/day12_full.txt", part2, 65402)
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


if __name__ == "__main__":
    main()
