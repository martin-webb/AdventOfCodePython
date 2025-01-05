from functools import cmp_to_key
from math import floor
from time import time

DAY = 5
NAME = "Print Queue"


def parse_rules(rules_input: str) -> set[tuple[int, int]]:
    """
    Parse input to return a set of 2-tuples of page dependency pairs.
    """
    rules: set[tuple[int, int]] = set()

    for line in rules_input.split("\n"):
        a, b = [int(n) for n in line.split("|")]
        rules.add((a, b))

    return rules


def part1(input: str) -> int:
    total = 0

    rules_input, updates_input = input.strip().split("\n\n")

    rules = parse_rules(rules_input)

    for update in updates_input.split("\n"):
        pages = [int(n) for n in update.split(",")]

        sorted_pages = sorted(
            pages, key=cmp_to_key(lambda a, b: -1 if (a, b) in rules else 1))

        if pages == sorted_pages:
            # Assuming odd number of pages so there's always a middle
            middle_index = int(floor(len(pages) / 2.0))
            total += pages[middle_index]

    return total


def part2(input: str) -> int:
    total = 0

    rules_input, updates_input = input.strip().split("\n\n")

    rules = parse_rules(rules_input)

    for update in updates_input.split("\n"):
        pages = [int(x) for x in update.split(",")]

        sorted_pages = sorted(
            pages, key=cmp_to_key(lambda a, b: -1 if (a, b) in rules else 1))

        if pages != sorted_pages:
            # Assuming odd number of pages so there's always a middle
            middle_index = int(floor(len(pages) / 2.0))
            total += sorted_pages[middle_index]

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day05_example.txt", part1, 143),
        ("Part 1", "inputs/day05_full.txt", part1, 4462),
        ("Part 2", "inputs/day05_example.txt", part2, 123),
        ("Part 2", "inputs/day05_full.txt", part2, 6767),
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
