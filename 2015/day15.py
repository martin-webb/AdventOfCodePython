from pathlib import Path
from time import time
from typing import Iterable

YEAR = 2015
DAY = 15
NAME = "Science for Hungry People"

Ingredient = tuple[str, tuple[int, ...], int]


def parse_line(line: str) -> Ingredient:
    name, values = line.split(": ")
    value_strings = values.split(", ")
    properties = tuple([int(s.split(" ")[1]) for s in value_strings[:-1]])
    calories = int(value_strings[-1].split(" ")[1])
    return name, properties, calories


def parse_input(input: str) -> list[Ingredient]:
    ingredients: list[Ingredient] = list()
    for line in input.strip().split("\n"):
        ingredients.append(parse_line(line))
    return ingredients


def partitions(n: int, k: int) -> Iterable[tuple[int, ...]]:
    """
    Generate all k-length partitions of n.
    """
    def _partitions(
            n: int,
            i: int,
            k: int,
            values: tuple[int, ...]
            ) -> Iterable[tuple[int, ...]]:
        if i == k-1:
            yield values + (n,)
        else:
            for m in range(n, -1, -1):
                for p in _partitions(n-m, i+1, k, values + (m,)):
                    yield p
    yield from _partitions(n, 0, k, tuple())


def product(values: list[int]) -> int:
    """
    Like sum() but for multiplication.
    """
    p = 1
    for n in values:
        p *= n
    return p


def part1(input: str) -> int:
    ingredients = parse_input(input)
    num_properties = len(ingredients[0][1])

    max_total = float("-inf")
    for p in partitions(100, len(ingredients)):
        subtotals = [0] * num_properties
        for i in range(num_properties):
            subtotals[i] = max(
                sum([n * ingredients[j][1][i] for j, n in enumerate(p)]), 0
            )
        total = product(subtotals)
        max_total = max(max_total, total)

    return int(max_total)


def part2(input: str) -> int:
    ingredients = parse_input(input)
    num_properties = len(ingredients[0][1])

    max_total = float("-inf")
    for p in partitions(100, len(ingredients)):
        subtotals = [0] * num_properties
        for i in range(num_properties):
            subtotals[i] = max(
                sum([n * ingredients[j][1][i] for j, n in enumerate(p)]), 0
            )

        calories = sum([n * ingredients[j][2] for j, n in enumerate(p)])
        if calories == 500:
            total = product(subtotals)
            max_total = max(max_total, total)

    return int(max_total)


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day15_example.txt", part1, 62842880),
        ("Part 1", "inputs/day15_full.txt", part1, 13882464),
        ("Part 1", "inputs/day15_example.txt", part2, 57600000),
        ("Part 1", "inputs/day15_full.txt", part2, 11171160)
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
