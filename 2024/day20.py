from collections import deque
from dataclasses import dataclass
from functools import partial
from itertools import permutations
from pathlib import Path
from time import time

YEAR = 2024
DAY = 20
NAME = "Race Condition"


@dataclass(eq=True, frozen=True)
class Vec2i:
    x: int
    y: int


DIRECTIONS = [
    Vec2i(0, -1),
    Vec2i(0, 1),
    Vec2i(-1, 0),
    Vec2i(1, 0)
]


def compute_distances(
    M: dict[Vec2i, str],
    start: Vec2i,
    end: Vec2i
) -> dict[Vec2i, int]:
    """
    Compute map of points to distances from the given start point.
    Unreachable points are not included in the map (over being assigned an
    infinite distance, for example).
    """
    distances: dict[Vec2i, int] = dict()

    to_visit = deque([(start, 0)])
    visited: set[Vec2i] = set()

    while to_visit:
        p, distance = to_visit.popleft()

        distances[p] = distance
        visited.add(p)

        next_positions = [Vec2i(p.x + d.x, p.y + d.y) for d in DIRECTIONS]
        for np in next_positions:
            if np not in visited and (M[np] == "." or np == end):
                to_visit.append((np, distance + 1))

    return distances


def num_cheats_two_ahead(
    M: dict[Vec2i, str],
    distances: dict[Vec2i, int],
    size: Vec2i,
    min_saving: int
) -> int:
    """
    Compute number of cheats that can be done by moving two steps through a
    wall in any cardinal direction from any point on the track, where that
    cheat would save at least the given minimum in time.
    """
    num_cheats = 0

    for y in range(size.y):
        for x in range(size.x):
            p0 = Vec2i(x, y)
            # Not a position on the path
            if p0 not in distances:
                continue

            for d in DIRECTIONS:
                p1 = Vec2i(p0.x + d.x, p0.y + d.y)
                p2 = Vec2i(p0.x + (d.x * 2), p0.y + (d.y * 2))
                # Check that we pass through a wall a wall in order for this
                # to be a valid cheat (that is, we can't just teleport two
                # steps). We don't check if we're heading in the same direction
                # (and so not through a wall) as this wouldn't catch diagonal
                # movements that also aren't cheats (and what direction is a
                # corner anyway).
                if M[p1] == "#" and p2 in distances:
                    d1 = distances[p0]
                    d2 = distances[p2]
                    if d2 > d1:
                        saving = d2 - d1 - 2
                        if saving >= min_saving:
                            num_cheats += 1

    return num_cheats


def num_cheats_within_distance(
    distances: dict[Vec2i, int],
    max_cheat_distance: int,
    min_saving: int
) -> int:
    """
    Compute number of unique cheats (ones that have a unique start and end
    position) that can be done by moving up to the given number of steps from
    any point on the track, where that cheat would save at least the given
    minimum in time.
    NOTE: This method doesn't check that a wall is passed through, so without
    an appropriate minimum cost saving we can find diagonal skips that are not
    actual cheats.
    """
    cheats: set[tuple[Vec2i, Vec2i]] = set()

    for p1, p2 in permutations(distances.keys(), 2):
        distance = abs(p1.x - p2.x) + abs(p1.y - p2.y)
        if distance <= max_cheat_distance:
            d1 = distances[p1]
            d2 = distances[p2]
            saving = d2 - d1 - distance
            if saving >= min_saving:
                cheats.add((p1, p2))

    return len(cheats)


def part1(input: str, min_saving: int) -> int:
    M: dict[Vec2i, str] = dict()

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            p = Vec2i(x, y)
            M[p] = char
            if char == "S":
                start = p
            elif char == "E":
                end = p

    size = Vec2i(x+1, y+1)

    distances: dict[Vec2i, int] = compute_distances(M, start, end)
    num_cheats = num_cheats_two_ahead(M, distances, size, min_saving)
    return num_cheats


def part2(input: str, min_saving: int) -> int:
    M: dict[Vec2i, str] = dict()

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            p = Vec2i(x, y)
            M[p] = char
            if char == "S":
                start = p
            elif char == "E":
                end = p

    distances: dict[Vec2i, int] = compute_distances(M, start, end)
    num_cheats = num_cheats_within_distance(distances, 20, min_saving)
    return num_cheats


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day20_example.txt",
         partial(part1, min_saving=0), 44),
        ("Part 1", "inputs/day20_full.txt",
         partial(part1, min_saving=100), 1358),
        ("Part 2", "inputs/day20_example.txt",
         partial(part2, min_saving=50), 285),
        ("Part 2", "inputs/day20_full.txt",
         partial(part2, min_saving=100), 1005856),
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
