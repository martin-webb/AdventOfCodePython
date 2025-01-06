from functools import cache
from pathlib import Path
from time import time

YEAR = 2023
DAY = 12
NAME = "Hot Springs"


def hsh(pattern: str, counts: tuple[int, ...], num: int = 0) -> int:
    # Adding a hash but we've already finished all groups
    if len(counts) == 0:
        return 0

    # This hash would make the current group too long
    too_long = (num + 1 > counts[0])
    if too_long:
        return 0

    is_last_character = (len(pattern) == 1)
    if is_last_character:
        # '#' groups are either closed with a following '.' OR with the final
        # character in the pattern (whether '#' or '?' leading to '#' branch)
        group_finished = (num + 1 == counts[0])
        if group_finished:
            return 1
        else:
            return 0
    else:
        return solve(pattern[1:], counts, num + 1)


def dot(pattern: str, counts: tuple[int, ...], num: int = 0) -> int:
    is_last_character = (len(pattern) == 1)
    if is_last_character:
        # Unfinished group but this '.' may finish it
        unfinished_groups = len(counts) > 0
        if unfinished_groups:
            is_group_finished = (num == counts[0])
            if is_group_finished:
                return 1
            else:
                return 0
        # No unfinished groups at the last character, this is a valid solution
        else:
            return 1
    else:
        unfinished_groups = len(counts) > 0
        if unfinished_groups:
            is_group_finished = (num == counts[0])
            is_group_not_started = (num == 0)
            if is_group_finished:
                return solve(pattern[1:], counts[1:], 0)
            elif is_group_not_started:
                return solve(pattern[1:], counts, 0)
            else:
                return 0
        else:
            return solve(pattern[1:], counts, 0)


@cache
def solve(pattern: str, counts: tuple[int, ...], num: int = 0) -> int:
    remaining_to_fill = (sum(counts) + (len(counts) - 1)) - num
    if len(pattern) < remaining_to_fill:
        return 0

    if pattern[0] == "#":
        return hsh(pattern, counts, num)
    elif pattern[0] == ".":
        return dot(pattern, counts, num)
    elif pattern[0] == "?":
        return hsh(pattern, counts, num) + dot(pattern, counts, num)
    else:
        raise RuntimeError(f"Invalid character '{pattern[0]}'")


def part1(input: str) -> int:
    total = 0

    for line in input.strip().split("\n"):
        pattern, counts_str = line.split()
        counts = tuple(int(n) for n in counts_str.split(","))
        total += solve(pattern, counts)

    return total


def part2(input: str) -> int:
    total = 0

    for line in input.strip().split("\n"):
        pattern, counts_str = line.split()
        pattern = "?".join(pattern for i in range(5))
        counts_str = ",".join(counts_str for i in range(5))
        counts = tuple(int(n) for n in counts_str.split(","))
        total += solve(pattern, counts)

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day12_example.txt", part1, 21),
        ("Part 1", "inputs/day12_full.txt", part1, 7922),
        ("Part 2", "inputs/day12_example.txt", part2, 525152),
        ("Part 2", "inputs/day12_full.txt", part2, 18093821750095),
    ):
        path = Path(__file__).parent / filename
        with open(path) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
