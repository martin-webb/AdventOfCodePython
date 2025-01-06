from dataclasses import dataclass
from pathlib import Path
from time import time

YEAR = 2023
DAY = 4
NAME = "Scratchcards"


@dataclass
class LineResult:
    card_num: int
    points: int


def points_for_line_part1(line: str) -> int:
    points = 0

    line = line.strip()
    nums_str = line.split(":")[1]
    winning_str, have_str = nums_str.split("|")
    winning = [int(n) for n in winning_str.split()]
    have = set([int(n) for n in have_str.split()])

    for n in winning:
        if n in have:
            if points == 0:
                points = 1
            else:
                points *= 2

    return points


def points_for_line_part2(line: str) -> LineResult:
    points = 0

    line = line.strip()
    card_str, nums_str = line.split(":")
    card_num = int(card_str.split()[1])
    winning_str, have_str = nums_str.split("|")
    winning = [int(n) for n in winning_str.split()]
    have = set([int(n) for n in have_str.split()])

    for n in winning:
        if n in have:
            points += 1

    result = LineResult(card_num=card_num, points=points)
    return result


def card_num_for_line(line: str) -> int:
    return int(line.split()[1].rstrip(":"))


def part1(input: str) -> int:
    points = 0

    for line in input.strip().split("\n"):
        points += points_for_line_part1(line)

    return points


def part2(input: str) -> int:
    lines = input.strip().split("\n")

    counts = [1] * len(lines)

    for line in lines:
        card_num = card_num_for_line(line)
        multiplier = counts[card_num - 1]
        result = points_for_line_part2(line)
        for i in range(card_num + 1, card_num + 1 + result.points):
            counts[i - 1] += multiplier

    total = sum(counts)
    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day04_example.txt", part1, 13),
        ("Part 1", "inputs/day04_full.txt", part1, 25174),
        ("Part 2", "inputs/day04_example.txt", part2, 30),
        ("Part 2", "inputs/day04_full.txt", part2, 6420979),
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
