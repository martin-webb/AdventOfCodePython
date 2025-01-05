from functools import cache
from time import time

DAY = 19
NAME = "Linen Layout"


@cache
def solve(cloths: frozenset, pattern: str) -> int:
    n = 0

    if len(pattern) > 0:
        for cloth in cloths:
            if pattern.startswith(cloth):
                n += solve(cloths, pattern[len(cloth):])
    else:
        n += 1

    return n


def part1(input: str) -> int:
    cloths_text, patterns_text = input.strip().split("\n\n")
    cloths = frozenset(cloths_text.split(", "))

    valid = 0
    for pattern in patterns_text.split("\n"):
        if solve(cloths, pattern) > 0:
            valid += 1

    return valid


def part2(input: str) -> int:
    cloths_text, patterns_text = input.strip().split("\n\n")
    cloths = frozenset(cloths_text.split(", "))

    valid = 0
    for pattern in patterns_text.split("\n"):
        valid += solve(cloths, pattern)

    return valid


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day19_example.txt", part1, 6),
        ("Part 1", "inputs/day19_full.txt", part1, 333),
        ("Part 2", "inputs/day19_example.txt", part2, 16),
        ("Part 2", "inputs/day19_full.txt", part2, 678536865274732),
    ):
        with open(filename) as f:
            contents = f.read()

        # Different inputs and puzzle parts should not interfere (in order to
        # get more accurate per-part timing)
        solve.cache_clear()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
