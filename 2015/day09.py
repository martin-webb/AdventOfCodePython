from itertools import permutations
from pathlib import Path
from time import time

YEAR = 2015
DAY = 9
NAME = "All in a Single Night"


def parse_input(input: str) -> tuple[set[str], dict[tuple[str, str], int]]:
    locations: set[str] = set()
    distances: dict[tuple[str, str], int] = dict()

    for line in input.strip().split("\n"):
        parts = line.split()
        src, dst, distance = parts[0], parts[2], int(parts[4])
        locations.add(src)
        locations.add(dst)
        distances[(src, dst)] = distance
        distances[(dst, src)] = distance

    return locations, distances


def find_distances(
    locations: set[str],
    distances: dict[tuple[str, str], int]
) -> tuple[int, int]:
    shortest, longest = float("inf"), float("-inf")
    for route in permutations(locations, len(locations)):
        distance = sum([distances[(a, b)] for a, b in zip(route, route[1:])])
        shortest, longest = min(shortest, distance), max(longest, distance)
    return int(shortest), int(longest)


def part1(input: str) -> int:
    locations, distances = parse_input(input)
    shortest, _ = find_distances(locations, distances)
    return shortest


def part2(input: str) -> int:
    locations, distances = parse_input(input)
    _, _longest = find_distances(locations, distances)
    return _longest


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day09_example.txt", part1, 605),
        ("Part 1", "inputs/day09_full.txt", part1, 251),
        ("Part 2", "inputs/day09_example.txt", part2, 982),
        ("Part 2", "inputs/day09_full.txt", part2, 898)
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
