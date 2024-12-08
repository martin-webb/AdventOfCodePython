from collections import defaultdict
from itertools import combinations
from time import time

DAY = 8
NAME = "Resonant Collinearity"


def find_antinodes(
    origin: tuple[int, int],
    direction: tuple[int, int],
    offset: int,
    width: int,
    height: int
) -> list[tuple[int, int]]:
    """
    Find antinode positions starting from origin in the given direction
    (direction here is a complete offset and not e.g. a unit vector), taking
    into account the given starting offset.
    Positive offsets move ahead in the given direction, while negative ones
    allow us to look 'behind' the direction of travel (this property is used
    for part 2.)
    """
    antinodes: list[tuple[int, int]] = list()

    while True:
        x = origin[0] + (direction[0] * offset)
        y = origin[1] + (direction[1] * offset)
        # Only include antinodes in the map, stopping once we're out of bounds
        if (0 <= x < width) and (0 <= y < height):
            antinodes.append((x, y))
            offset += 1
        else:
            break

    return antinodes


def part1(input: str) -> int:
    M: dict[str, set[tuple[int, int]]] = defaultdict(set)

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            if char != ".":
                M[char].add((x, y))

    w, h = x + 1, y + 1

    antinodes: list[tuple[int, int]] = list()
    for positions in M.values():
        for p1, p2 in combinations(positions, 2):
            dx = abs(p1[0] - p2[0])
            dy = abs(p1[1] - p2[1])

            if p1[0] < p2[0]:
                if p1[1] < p2[1]:
                    antinodes += find_antinodes(p1, (-dx, -dy), 1, w, h)[:1]
                    antinodes += find_antinodes(p2, (dx, dy), 1, w, h)[:1]
                else:
                    antinodes += find_antinodes(p1, (-dx, dy), 1, w, h)[:1]
                    antinodes += find_antinodes(p2, (dx, -dy), 1, w, h)[:1]
            else:
                if p1[1] < p2[1]:
                    antinodes += find_antinodes(p1, (dx, -dy), 1, w, h)[:1]
                    antinodes += find_antinodes(p2, (-dx, dy), 1, w, h)[:1]
                else:
                    antinodes += find_antinodes(p1, (dx, dy), 1, w, h)[:1]
                    antinodes += find_antinodes(p2, (-dx, -dy), 1, w, h)[:1]

    unique_antinodes = set(antinodes)
    return len(unique_antinodes)


def part2(input: str) -> int:
    """
    The same as part 1 but with two changes:
    - The 'offset' parameter for find_antinodes() is -1 (to look behind)
    - The results from find_antinodes() are not limited to 1
    """
    M: dict[str, set[tuple[int, int]]] = defaultdict(set)

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            if char != ".":
                M[char].add((x, y))

    w, h = x + 1, y + 1

    antinodes: list[tuple[int, int]] = list()
    for positions in M.values():
        for p1, p2 in combinations(positions, 2):
            dx = abs(p1[0] - p2[0])
            dy = abs(p1[1] - p2[1])

            if p1[0] < p2[0]:
                if p1[1] < p2[1]:
                    antinodes += find_antinodes(p1, (-dx, -dy), -1, w, h)
                    antinodes += find_antinodes(p2, (dx, dy), -1, w, h)
                else:
                    antinodes += find_antinodes(p1, (-dx, dy), -1, w, h)
                    antinodes += find_antinodes(p2, (dx, -dy), -1, w, h)
            else:
                if p1[1] < p2[1]:
                    antinodes += find_antinodes(p1, (dx, -dy), -1, w, h)
                    antinodes += find_antinodes(p2, (-dx, dy), -1, w, h)
                else:
                    antinodes += find_antinodes(p1, (dx, dy), -1, w, h)
                    antinodes += find_antinodes(p2, (-dx, -dy), -1, w, h)

    unique_antinodes = set(antinodes)
    return len(unique_antinodes)


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day08_example.txt", part1, 14),
        ("Part 1", "inputs/day08_full.txt", part1, 367),
        ("Part 2", "inputs/day08_example.txt", part2, 34),
        ("Part 2", "inputs/day08_full.txt", part2, 1285),
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
