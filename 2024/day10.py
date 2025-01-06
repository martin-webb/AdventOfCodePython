from collections import defaultdict
from pathlib import Path
from time import time

YEAR = 2024
DAY = 10
NAME = "Hoof It"


def follow(
        M: dict[int, dict[int, int]],
        size: tuple[int, int],
        position: tuple[int, int],
        height: int,
        visited: list[tuple[int, int]]
) -> None:
    """
    Follow map from starting position and return all visited 9-height positions
    reached via all paths.
    The returned positions can include duplicates if reached via multiple
    unique paths (this is used to support both parts 1 and 2).
    """
    if height < 9:
        neighbours = [
            (position[0], position[1] - 1),
            (position[0], position[1] + 1),
            (position[0] - 1, position[1]),
            (position[0] + 1, position[1]),
        ]
        for neighbour in neighbours:
            if 0 <= neighbour[0] < size[0] and 0 <= neighbour[1] < size[1]:
                if M[neighbour[1]][neighbour[0]] == height + 1:
                    follow(M, size, neighbour, height + 1, visited)
    else:
        visited.append(position)


def part1(input: str) -> int:
    M: dict[int, dict[int, int]] = defaultdict(dict)
    trailheads: list[tuple[int, int]] = list()

    for y, line in enumerate(input.strip().split("\n")):
        for x, height in enumerate(line):
            M[y][x] = int(height)
            if M[y][x] == 0:
                trailheads.append((x, y))

    size = (x + 1, y + 1)

    total = 0
    for trailhead in trailheads:
        visited: list[tuple[int, int]] = list()
        follow(M, size, trailhead, 0, visited)
        total += len(set(visited))

    return total


def part2(input: str) -> int:
    M: dict[int, dict[int, int]] = defaultdict(dict)
    trailheads: list[tuple[int, int]] = list()

    for y, line in enumerate(input.strip().split("\n")):
        for x, height in enumerate(line):
            M[y][x] = int(height)
            if M[y][x] == 0:
                trailheads.append((x, y))

    size = (x + 1, y + 1)

    total = 0
    for trailhead in trailheads:
        visited: list[tuple[int, int]] = list()
        follow(M, size, trailhead, 0, visited)
        total += len(visited)

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day10_example.txt", part1, 36),
        ("Part 1", "inputs/day10_full.txt", part1, 489),
        ("Part 2", "inputs/day10_example.txt", part2, 81),
        ("Part 2", "inputs/day10_full.txt", part2, 1086),
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
