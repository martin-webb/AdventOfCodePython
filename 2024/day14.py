from collections import defaultdict
from functools import partial
from math import ceil
from pathlib import Path
from time import time
from typing import cast

YEAR = 2024
DAY = 14
NAME = "Restroom Redoubt"


def grid_counts(
    data: list[int],
    width: int,
    height: int,
    grid_width: int,
    grid_height: int
) -> list[int]:
    """
    Return a vector of counts of the elements of input count vector, quantised
    into a grid defined by the given parameters.
    """
    counts = [0] * (ceil(width / grid_width) * ceil(height / grid_height))

    for y in range(height):
        grid_y = y // grid_height
        for x in range(width):
            grid_x = x // grid_width
            counts[grid_y * grid_width + grid_x] += data[y * width + x]

    return counts


def part1(input: str, width: int, height: int) -> int:
    counts: dict[tuple[int, int], int] = defaultdict(int)
    n = 100

    for line in input.strip().split("\n"):
        ps, vs = line.split()
        p = tuple(int(n) for n in ps.lstrip("p=").split(","))
        v = tuple(int(n) for n in vs.lstrip("v=").split(","))
        x = (p[0] + v[0] * n) % width
        y = (p[1] + v[1] * n) % height
        counts[(x, y)] += 1

    quadrants = [[0, 0], [0, 0]]
    for y in range(height):
        # Skip the middle row
        if y != (height - 1) / 2:
            for x in range(width):
                # Skip the middle column
                if x != (width - 1) / 2:
                    q_y = 0 if y < (height / 2) else 1
                    q_x = 0 if x < (width / 2) else 1
                    quadrants[q_y][q_x] += counts[(x, y)]

    safety = \
        quadrants[0][0] * quadrants[0][1] * quadrants[1][0] * quadrants[1][1]
    return safety


def part2(
    input: str,
    width: int,
    height: int,
    grid_width: int,
    grid_height: int,
    difference_threshold: float
) -> int:
    """
    Inspired by the safety number calculation from part 1, where the map is
    quantised into four quadrants and a single value is calculated for each of
    those areas before those values are used to derived a final value, here we
    also quantise the count data into a grid, sum the counts from each area,
    then compare the quantised counts from each iteration with the initial
    state of the simulation.
    This is based on the idea that when the robots are not forming a Christmas
    tree shape their distribution across the map should be (somewhat) uniform,
    but when they form the tree shape there will be a significantly increased
    robot count in one or more of the grid areas.
    By computing a difference value between two sets of quantised counts, robot
    distributions that are mostly uniform will result in a low difference
    value, while a robot distribution that forms the Christmas tree should
    result in a larger difference value.
    Our search for the elusive robot Christmas tree therefore works by
    iterating the simulation until it looks like the robots are significantly
    clustered.
    The actual values used in the final part 2 solution were determined
    iteratively. Having found the Christmas tree, the grid size was adjusted to
    be closer to the actual robot layout and the threshold was adjusted to
    match.
    """
    robots: list[tuple[tuple[int, int], tuple[int, int]]] = list()

    for line in input.strip().split("\n"):
        ps, vs = line.split()
        p = tuple(int(n) for n in ps.lstrip("p=").split(","))
        v = tuple(int(n) for n in vs.lstrip("v=").split(","))
        robots.append((cast(tuple[int, int], p), cast(tuple[int, int], v)))

    counts: list[int] = [0] * width * height
    for robot in robots:
        x, y = robot[0]
        counts[y * width + x] += 1

    original_counts_grid = \
        grid_counts(counts, width, height, grid_width, grid_height)

    n = 1
    while True:
        counts = [0] * width * height
        for p, v in robots:
            x = (p[0] + v[0] * n) % width
            y = (p[1] + v[1] * n) % height
            counts[y * width + x] += 1

        counts_grid = \
            grid_counts(counts, width, height, grid_width, grid_height)

        difference = sum(
            abs(a-b) for a, b in zip(original_counts_grid, counts_grid)
        )

        if difference > difference_threshold:
            break

        n += 1

    return n


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day14_example.txt",
         partial(part1, width=11, height=7), 12),
        ("Part 1", "inputs/day14_full.txt",
         partial(part1, width=101, height=103), 218433348),
        ("Part 2", "inputs/day14_full.txt",
         partial(part2, width=101, height=103,
                 grid_width=3, grid_height=3, difference_threshold=450), 6512),
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
