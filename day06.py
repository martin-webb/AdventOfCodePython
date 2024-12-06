from collections import defaultdict
from time import time
from typing import Optional

DAY = 6
NAME = "Guard Gallivant"

TURNS_CW = {
    (-1, 0): (0, -1),
    (1, 0): (0, 1),
    (0, -1): (1, 0),
    (0, 1): (-1, 0)
}


def walk_line(
        map: dict[int, dict[int, str]],
        size: tuple[int, int],
        position: tuple[int, int],
        direction: tuple[int, int],
        visited: set[tuple[tuple[int, int], tuple[int, int]]]
) -> tuple[Optional[tuple[int, int]], Optional[tuple[int, int]], bool]:
    """
    Walks a single straight line of the path taken by the guard across the map,
    starting from the given position and moving in the given direction.
    Returns the resulting position at the end of the line (either after hitting
    an obstacle or getting to the edge of the map), the next direction of
    travel after turning (if having hit an obstacle) and a boolean to indicate
    if we ended up in a loop (used for part 2).
    """
    next_direction = None

    while True:
        visited.add((position, direction))
        next_position = (position[0]+direction[0], position[1]+direction[1])
        if (
            next_position[0] < 0
            or next_position[0] >= size[0]
            or next_position[1] < 0
            or next_position[1] >= size[1]
        ):
            break

        next_square = map[next_position[1]][next_position[0]]
        if next_square == "#":
            next_direction = TURNS_CW[direction]
            break

        position = next_position

        if (next_position, direction) in visited:
            return None, None, True

    return position, next_direction, False


def walk(
        map: dict[int, dict[int, str]],
        size: tuple[int, int],
        position: tuple[int, int],
        direction: tuple[int, int],
) -> tuple[Optional[set[tuple[tuple[int, int], tuple[int, int]]]], bool]:
    """
    Walks the path taken by the guard across the map, starting from the given
    position and moving in the given direction.
    Returns a pair comprising a set of pairs of visited positions with the
    direction being followed at that position and a boolean to indicate whether
    the walk contains a loop (used for part 2).
    The set of pairs of visited positions with a direction allows us to cross
    the same square twice in different directions but detect when we're in a
    loop.
    """
    visited: set[tuple[tuple[int, int], tuple[int, int]]] = set()

    while direction is not None:
        position, direction, has_loop = \
            walk_line(map, size, position, direction, visited)  # type: ignore
        if has_loop:
            return None, True

    return visited, False


def part1(input: str) -> int:
    map: dict[int, dict[int, str]] = defaultdict(dict)

    position = None
    direction = (0, -1)  # Hardcoded up as initial direction

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            if char == "^":
                position = (x, y)
                char = "."
            map[y][x] = char

    size = x + 1, y + 1

    assert position is not None
    assert direction is not None

    visited, _ = walk(map, size, position, direction)

    assert visited is not None

    visited_positions = set([v[0] for v in visited])

    return len(visited_positions)


def part2(input: str) -> int:
    map: dict[int, dict[int, str]] = defaultdict(dict)

    position = None
    direction = (0, -1)  # Hardcoded up as initial direction

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            if char == "^":
                char = "."
                position = (x, y)
            map[y][x] = char

    size = x + 1, y + 1

    assert position is not None
    assert direction is not None

    # Initial traversal (without loop) to find the path that the guard walks
    visited, _ = walk(map, size, position, direction)

    assert visited is not None

    visited_positions = set([v[0] for v in visited])

    # Generate potential obstacle locations to test from the path walked by the
    # guard.
    # There are a number of filters that could be applied to exclude potential
    # obstacle positions so we don't need to generate a map variation and test
    # it for a loop, however given the map structure (size, path and number of
    # existing obstacles) most of these don't make a significant impact on run
    # time (a more sparse map and/or longer time required to check for a loop
    # might make these additional checks more useful) so haven't been included.
    # We do include the following checks:
    # - Exclude the starting position
    # - Exclude positions not on the known path (these will NEVER be hit)
    # We don't include the following checks:
    # - Exclude positions that aren't one-ahead from the horizontal or vertical
    #   line of an adjacent rock (depending on the direction of travel) as we
    #   need to hit another obstacle after being turned by any obstacle we add,
    #   so they would need to be offset by one)
    # - Exclude positions that aren't on the same side as would be turned to
    #   after hitting an obstacle straight ahead
    obstacles: set[tuple[int, int]] = set()
    for p in visited_positions:
        if p != position:
            obstacles.add(p)

    num_loops = 0

    for o in obstacles:
        # Update map in place then restore to original state instead of copying
        # Small optimisation that saves ~0.5s
        # index = o[1] * size[0] + o[0]
        original = map[o[1]][o[0]]
        map[o[1]][o[0]] = "#"
        _, has_loop = walk(map, size, position, direction)
        map[o[1]][o[0]] = original

        if has_loop:
            num_loops += 1

    return num_loops


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day06_example.txt", part1, 41),
        ("Part 1", "inputs/day06_full.txt", part1, 5080),
        ("Part 2", "inputs/day06_example.txt", part2, 6),
        ("Part 2", "inputs/day06_full.txt", part2, 1919),
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
