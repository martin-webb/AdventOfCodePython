from collections import deque
from pathlib import Path
from io import StringIO
from time import time

YEAR = 2016
DAY = 13
NAME = "A Maze of Twisty Little Cubicles"


def make_map(
        size: tuple[int, int],
        favourite_number: int
        ) -> dict[tuple[int, int], str]:
    grid: dict[tuple[int, int], str] = dict()

    for y in range(size[1]):
        for x in range(size[0]):
            n = x*x + x*3 + 2*x*y + y + y*y
            n += favourite_number
            num_bits = n.bit_count()
            grid[(x, y)] = "." if num_bits % 2 == 0 else "#"

    return grid


def draw(grid: dict[tuple[int, int], str]) -> str:
    s = StringIO()

    width = max(k[0] for k in grid.keys())
    height = max(k[1] for k in grid.keys())

    for y in range(height):
        for x in range(width):
            s.write(grid[(x, y)])
        s.write("\n")
    return s.getvalue()


def find_distances(
        grid: dict[tuple[int, int], str],
        start: tuple[int, int]
        ) -> dict[tuple[int, int], int]:
    """
    Flood fill approach to find distances to cubicles.
    """
    distances: dict[tuple[int, int], int] = dict()
    visited: set[tuple[int, int]] = set()

    Q = deque([(start, 0)])
    while Q:
        current, distance = Q.popleft()

        distances[current] = distance
        visited.add(current)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            neighbour = (current[0] + direction[0], current[1] + direction[1])
            if neighbour in visited:
                continue
            if neighbour not in grid:
                continue
            if grid[neighbour] == "#":
                continue
            Q.append((neighbour, distance+1))

    return distances


def part1(input: str) -> int:
    favourite_number = int(input.strip())
    begin = (1, 1)
    end = (31, 39)

    # XXX: Map size exactly as bag as it needs to be to contain the end point
    # This is a feature of the input, as this indicates we don't need to loop
    # or double back
    size = (32, 40)

    grid = make_map(size, favourite_number)
    # print(draw(grid))
    distances = find_distances(grid, begin)
    result = distances[end]
    return result


def part2(input: str) -> int:
    favourite_number = int(input.strip())
    begin = (1, 1)

    # XXX: Using same map size as for part 1 as this is enough to account for
    # the target distance (it's actually more than and we can make a smaller
    # map, but this feels neat and it's fast enough)
    size = (32, 40)

    grid = make_map(size, favourite_number)
    # print(draw(grid))
    distances = find_distances(grid, begin)
    within_50 = [v for v in distances.values() if v <= 50]
    result = len(within_50)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day13_full.txt", part1, 82),
        ("Part 2", "inputs/day13_full.txt", part2, 138),
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
