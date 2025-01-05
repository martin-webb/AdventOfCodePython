import re
from time import time

DAY = 3
NAME = "Mull It Over"


def part1(input: str) -> int:
    total = 0

    matches = re.findall(r"(mul)\(([0-9]+,[0-9]+)?\)", input)
    for m in matches:
        a, b = [int(n) for n in m[1].split(",")]
        total += a * b

    return total


def part2(input: str) -> int:
    total = 0

    enabled = True
    matches = re.findall(r"(mul|do|don't)\(([0-9]+,[0-9]+)?\)", input)
    for m in matches:
        if m[0] == "mul":
            if enabled:
                a, b = [int(n) for n in m[1].split(",")]
                total += a * b
        elif m[0] == "do":
            enabled = True
        elif m[0] == "don't":
            enabled = False

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day03_part1_example.txt", part1, 161),
        ("Part 1", "inputs/day03_full.txt", part1, 184576302),
        ("Part 2", "inputs/day03_part2_example.txt", part2, 48),
        ("Part 2", "inputs/day03_full.txt", part2, 118173507),
    ):
        with open(filename) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
