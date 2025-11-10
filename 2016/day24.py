from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import pairwise, permutations
from pathlib import Path
import sys
from time import time

YEAR = 2016
DAY = 24
NAME = "Air Duct Spelunking"


@dataclass(frozen=True)
class DistanceValue:
    num: int  # Destination point number
    distance: int


def make_grid(input: str) -> list[list[str]]:
    grid: list[list[str]] = list()

    for line in input.strip().split("\n"):
        grid.append(list(line))

    return grid


def find_points_of_interest(
        grid: list[list[str]]
        ) -> dict[int, tuple[int, int]]:
    points_of_interest: dict[int, tuple[int, int]] = dict()

    x_max, y_max = len(grid[0]), len(grid)  # Exclusive

    for y in range(y_max):
        for x in range(x_max):
            c = grid[y][x]
            if c.isdigit():
                n = int(c)
                points_of_interest[n] = (x, y)

    return points_of_interest


def find_distances(
        grid: list[list[str]],
        src: tuple[int, int]
        ) -> list[DistanceValue]:
    """
    Breadth-first flood fill to find distances to all other points of interest
    in the grid from the given starting position.
    """
    distances: list[DistanceValue] = list()

    if not grid[src[1]][src[0]].isdigit():
        raise ValueError(f"Start cell ({src[0]}, {src[1]}) is not a digit")

    width, height = len(grid[0]), len(grid)
    seen: set[tuple[int, int]] = set([src])

    q = deque([(src, 0)])
    while q:
        p, distance = q.popleft()

        # Found a point of interest (that's not where we started)
        if grid[p[1]][p[0]].isdigit() and p != src:
            n = int(grid[p[1]][p[0]])
            distances.append(DistanceValue(num=n, distance=distance))

        # NOTE: We keep searching even if we've found a point of interest, as
        # we're allowed to backtrack through previously visited nodes, so we
        # want to just keep going and find every other point of interest from
        # the starting one (over finding immediate neighbours and then
        # stopping, for example)
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbour = (p[0] + direction[0], p[1] + direction[1])

            # Bounds check
            if not (0 <= neighbour[0] < width and 0 <= neighbour[1] < height):
                continue

            # Hit a wall?
            if grid[neighbour[1]][neighbour[0]] == "#":
                continue

            # Seen before
            if neighbour in seen:
                continue

            q.append((neighbour, distance+1))
            seen.add(neighbour)

    return distances


def build_adjacencies_with_distances(
        grid: list[list[str]],
        points_of_interest: dict[int, tuple[int, int]]
        ) -> dict[int, list[DistanceValue]]:
    adjacencies: dict[int, list[DistanceValue]] = defaultdict(list)

    for n, point in points_of_interest.items():
        distances = find_distances(grid, point)
        adjacencies[n] += distances

    return adjacencies


def build_distance_pairs(
        adjacencies: dict[int, list[DistanceValue]]
        ) -> dict[tuple[int, int], int]:
    distances: dict[tuple[int, int], int] = {}

    for n, A in adjacencies.items():
        for a in A:
            distances[(n, a.num)] = a.distance

    return distances


def solve(input: str, return_to_beginning: bool) -> int:
    """
    1. Flood fill from each point to all other points to determine distances
    2. Get all path permutations starting at 0 (and for part 2, ending at 0)
    3. Use the distance information from 1 to get the shortest distance between
    each point, allowing for backtracking through previously-visited points
    4. Try all the paths!
    """
    grid = make_grid(input)
    points_of_interest = find_points_of_interest(grid)
    adjacencies = build_adjacencies_with_distances(grid, points_of_interest)
    distances = build_distance_pairs(adjacencies)

    min_distance = sys.maxsize
    locations = set(adjacencies.keys())

    # We always start at 0, so don't build path permutations from this but
    # prepend it in later for the pairwise distance calculations
    locations_minus_0 = locations - {0}

    for permutation in permutations(locations_minus_0, len(locations_minus_0)):
        # We always start at 0
        permutation = (0,) + permutation

        # For part 2 we also need to return to location 0
        if return_to_beginning:
            permutation += (0,)

        distance = 0
        for pair in pairwise(permutation):
            distance += distances[pair]

        min_distance = min(min_distance, distance)

    return min_distance


def part1(input: str) -> int:
    return solve(input, return_to_beginning=False)


def part2(input: str) -> int:
    return solve(input, return_to_beginning=True)


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day24_example.txt", part1, 14),
        ("Part 1", "inputs/day24_full.txt", part1, 500),
        ("Part 2", "inputs/day24_full.txt", part2, 748),
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
