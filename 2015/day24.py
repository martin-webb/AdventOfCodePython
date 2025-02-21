from itertools import combinations
from pathlib import Path
from time import time

YEAR = 2015
DAY = 24
NAME = "It Hangs in the Balance"


def parse_input(input: str) -> list[int]:
    weights = [int(line) for line in input.strip().split("\n")]
    return weights


def product(values: tuple[int, ...]) -> int:
    """
    Like sum() but for multiplication.
    """
    p = 1
    for n in values:
        p *= n
    return p


def solve(weights: list[int], num_groups: int) -> int:
    min_qe = float("inf")

    # All groups must have an even weight, so we can simply discard any
    # combination we find for the first group that doesn't match the target
    target = sum(weights) // num_groups

    # Start with lower r-length combinations for the first group in order to
    # get lower potential QE values first
    for length in range(2, len(weights) - (num_groups - 1)):
        done = False
        for combination in combinations(weights, length):
            if sum(combination) != target:
                continue

            qe = product(combination)
            min_qe = min(qe, min_qe)
            done = True

        # Once we've found the min QE from one r-length combination group then
        # no group with more elements can possibly have a lower QE, so we can
        # stop searching
        if done:
            break

    return int(min_qe)


def part1(input: str) -> int:
    weights = parse_input(input)
    result = solve(weights, 3)
    return result


def part2(input: str) -> int:
    weights = parse_input(input)
    result = solve(weights, 4)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day24_full.txt", part1, 11846773891),
        ("Part 2", "inputs/day24_full.txt", part2, 80393059),
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
