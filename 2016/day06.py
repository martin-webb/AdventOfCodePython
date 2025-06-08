from collections import Counter
from pathlib import Path
from time import time

YEAR = 2016
DAY = 6
NAME = "Signals and Noise"


def solve(input: str, index: int) -> str:
    lines = input.strip().split("\n")

    counters: list[Counter] = list()
    for _ in range(len(lines[0])):
        counters.append(Counter())

    for line in lines:
        for i, char in enumerate(line):
            counters[i][char] += 1

    message = "".join(counter.most_common()[index][0] for counter in counters)
    return message


def part1(input: str) -> str:
    message = solve(input, 0)
    return message


def part2(input: str) -> str:
    message = solve(input, -1)
    return message


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day06_sample.txt", part1, "easter"),
        ("Part 1", "inputs/day06_full.txt", part1, "tzstqsua"),
        ("Part 2", "inputs/day06_sample.txt", part2, "advent"),
        ("Part 2", "inputs/day06_full.txt", part2, "myregdnr"),
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
