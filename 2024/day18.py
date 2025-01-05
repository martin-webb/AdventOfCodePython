from collections import deque
from functools import partial
from time import time

YEAR = 2024
DAY = 18
NAME = "RAM Run"

OFFSETS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0)
]


def shortest_distances(
    start: tuple[int, int],
    size: tuple[int, int],
    unreachable: set[tuple[int, int]],
) -> dict[tuple[int, int], int]:
    """
    Compute shortest distances from the given position to all other positions
    that are reachable in a grid of the given size, returning a map of
    positions to distances. Unreachable positions are not included in the
    output map (over having an infinite distance, for example).
    """
    distances: dict[tuple[int, int], int] = dict()

    to_visit = deque([(start, 0)])
    visited: set[tuple[int, int]] = set([start])

    while to_visit:
        pos, distance = to_visit.popleft()
        distances[pos] = distance
        neighbours = [(pos[0] + o[0], pos[1] + o[1]) for o in OFFSETS]
        for neighbour in neighbours:
            if 0 <= neighbour[0] < size[0] and 0 <= neighbour[1] < size[1]:
                if neighbour not in visited and neighbour not in unreachable:
                    visited.add(neighbour)
                    to_visit.append((neighbour, distance + 1))

    return distances


def part1(input: str, size: tuple[int, int], n: int) -> int:
    coords: list[tuple[int, int]] = list()
    for line in input.strip().split("\n"):
        x, y = [int(n) for n in line.split(",")]
        coords.append((x, y))

    unreachable: set[tuple[int, int]] = set()
    for coord in coords[:n]:
        unreachable.add(coord)

    start = (0, 0)
    end = (size[0] - 1, size[1] - 1)
    distances = shortest_distances(start, size, unreachable)
    shortest = distances[end]
    return shortest


def part2(input: str, size: tuple[int, int]) -> str:
    coords: list[tuple[int, int]] = list()
    for line in input.strip().split("\n"):
        x, y = [int(n) for n in line.split(",")]
        coords.append((x, y))

    unreachable: set[tuple[int, int]] = set()

    start = (0, 0)
    end = (size[0] - 1, size[1] - 1)

    for coord in coords:
        unreachable.add(coord)
        distances = shortest_distances(start, size, unreachable)
        if end not in distances:
            break

    return f"{coord[0]},{coord[1]}"


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day18_example.txt",
         partial(part1, size=(7, 7), n=12), 22),
        ("Part 1", "inputs/day18_full.txt",
         partial(part1, size=(71, 71), n=1024), 316),
        ("Part 2", "inputs/day18_example.txt",
         partial(part2, size=(7, 7)), "6,1"),
        ("Part 2", "inputs/day18_full.txt",
         partial(part2, size=(71, 71)), "45,18"),
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
