from pathlib import Path
from time import time
from itertools import chain, combinations, product
from math import ceil

YEAR = 2015
DAY = 21
NAME = "RPG Simulator 20XX"

WEAPONS = [
    (8, 4,  0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
]

ARMOR = [
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]

RINGS = [
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]


def parse_input(input: str) -> tuple[int, int, int]:
    for line in input.strip().split("\n"):
        parts = line.split(":")
        if parts[0] == "Hit Points":
            hp = int(parts[1])
        elif parts[0] == "Damage":
            damage = int(parts[1])
        elif parts[0] == "Armor":
            armor = int(parts[1])

    return hp, damage, armor


def solve(input: str) -> tuple[int, int]:
    boss_hp, boss_damage, boss_armor = parse_input(input)

    weapons = WEAPONS  # Always a weapon

    # Include a choice for no armor
    armor = chain(
        [(0, 0, 0),],
        ARMOR
    )

    # Include choices for no rings and one ring
    rings = chain(
        [((0, 0, 0), (0, 0, 0))],
        product(RINGS, [(0, 0, 0)]),
        combinations(RINGS, 2)
    )

    win_cost_min = float("inf")
    loss_cost_max = float("-inf")

    for equipment in product(weapons, armor, rings):
        cost = damage = armor_ = 0

        cost += equipment[0][0]
        damage += equipment[0][1]
        armor_ += equipment[0][2]

        cost += equipment[1][0]
        damage += equipment[1][1]
        armor_ += equipment[1][2]

        for ring in equipment[2]:
            cost += ring[0]
            damage += ring[1]
            armor_ += ring[2]

        num_player_attacks = ceil(boss_hp / max(damage - boss_armor, 1))
        num_boss_attacks = ceil(100 / max(boss_damage - armor_, 1))

        if num_player_attacks <= num_boss_attacks:
            win_cost_min = min(win_cost_min, cost)
        else:
            loss_cost_max = max(loss_cost_max, cost)

    return int(win_cost_min), int(loss_cost_max)


def part1(input: str) -> int:
    win_cost_min, _ = solve(input)
    return win_cost_min


def part2(input: str) -> int:
    _, loss_cost_max = solve(input)
    return loss_cost_max


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day21_full.txt", part1, 121),
        ("Part 2", "inputs/day21_full.txt", part2, 201),
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

        if label == "Part 2" and "full" in filename:
            assert result > 127


if __name__ == "__main__":
    main()
