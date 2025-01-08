from pathlib import Path
from time import time

YEAR = 2015
DAY = 2
NAME = "I Was Told There Would Be No Math"


def part1(input: str) -> int:
    result = 0

    for line in input.strip().split("\n"):
        l, w, h = [int(n) for n in line.split("x")]
        result += 2*l*w + 2*w*h + 2*h*l
        sorted_dimensions = sorted([l, w, h])
        result += sorted_dimensions[0] * sorted_dimensions[1]

    return result


def part2(input: str) -> int:
    result = 0

    for line in input.strip().split("\n"):
        l, w, h = [int(n) for n in line.split("x")]
        sorted_dimensions = sorted([l, w, h])
        result += 2 * sorted_dimensions[0] + 2 * sorted_dimensions[1]
        result += l*w*h

    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day02_example1.txt", part1, 58),
        ("Part 1", "inputs/day02_example2.txt", part1, 43),
        ("Part 1", "inputs/day02_full.txt", part1, 1586300),
        ("Part 2", "inputs/day02_example1.txt", part2, 34),
        ("Part 2", "inputs/day02_example2.txt", part2, 14),
        ("Part 2", "inputs/day02_full.txt", part2, 3737498),
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
