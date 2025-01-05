from math import floor
from time import time
from typing import Optional

DAY = 13
NAME = "Claw Contraption"


def parse_machine_description(s: str) -> tuple[int, int, int, int, int, int]:
    """
    Parse input and return a 6-tuple of:
    (Button A X, Button A Y, Button B X, Button B Y, Prize X, Prize Y)
    """
    button_a, button_b, prize = s.split("\n")
    ax = int(button_a.split(":")[1].split(",")[0].lstrip(" X+"))
    ay = int(button_a.split(":")[1].split(",")[1].lstrip(" Y+"))
    bx = int(button_b.split(":")[1].split(",")[0].lstrip(" X+"))
    by = int(button_b.split(":")[1].split(",")[1].lstrip(" Y+"))
    prize_x = int(prize.split(":")[1].split(",")[0].lstrip(" X="))
    prize_y = int(prize.split(":")[1].split(",")[1].lstrip(" Y="))
    return ax, ay, bx, by, prize_x, prize_y


def solve(
    ax: int,
    ay: int,
    bx: int,
    by: int,
    prize_x: int,
    prize_y: int
) -> Optional[tuple[int, int]]:
    """
    Determine number of A and B button presses for the given machine if a prize
    can be won or None if not.
    """
    # Two equations for each machine:
    # (1) a * ax + b * bx = prize_x
    # (2) a * ay + b * by = prize_y
    # Rewritten in terms of a:
    # (1) a = (prize_x - (b * bx)) / ax
    # (2) a = (prize_y - (b * by)) / ay
    # Equality:
    # (prize_x - (b * bx)) / ax = (prize_y - (b * by)) / ay
    # Rearrange and expand to to rewrite in terms of b:
    # ay * (prize_x - (b * bx)) = ax * (prize_y - (b * by))
    # b = (ax * prize_y) - (prize_x * ay) / ((ay * bx) + (ax * by))
    b = ((ax * prize_y) - (prize_x * ay)) / ((ax * by) - (ay * bx))
    # Subsitute b back into (1):
    a = (prize_x - (b * bx)) / ax
    return (int(a), int(b)) if floor(a) == a and floor(b) == b else None


def part1(input: str) -> int:
    a = 0
    b = 0

    for machine in input.strip().split("\n\n"):
        ax, ay, bx, by, prize_x, prize_y = parse_machine_description(machine)
        result = solve(ax, ay, bx, by, prize_x, prize_y)
        if result is not None:
            a += result[0]
            b += result[1]

    tokens = a * 3 + b
    return tokens


def part2(input: str) -> int:
    a = 0
    b = 0

    for machine in input.strip().split("\n\n"):
        ax, ay, bx, by, prize_x, prize_y = parse_machine_description(machine)
        prize_x += 10000000000000
        prize_y += 10000000000000

        result = solve(ax, ay, bx, by, prize_x, prize_y)
        if result is not None:
            a += result[0]
            b += result[1]

    tokens = a * 3 + b
    return tokens


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day13_example.txt", part1, 480),
        ("Part 1", "inputs/day13_full.txt", part1, 35997),
        ("Part 2", "inputs/day13_full.txt", part2, 82510994362072),
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
