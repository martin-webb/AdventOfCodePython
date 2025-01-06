from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from time import time

YEAR = 2024
DAY = 12
NAME = "Garden Groups"


@dataclass(eq=True, frozen=True, order=True)
class Point:
    x: int
    y: int


def follow_region(
    M: dict[int, dict[int, str]],
    pos: Point,
    region: list[Point],
    unvisited: set[Point]
) -> None:
    """
    Recursive region determination using global unvisited set to ignore
    positions we've checked in both parent function calls and separate
    invocations for other starting positions.
    """
    # Add the position to the region
    region.append(pos)

    # Never come here again
    unvisited.remove(pos)

    width, height = len(M[0]), len(M)
    neighbours = [
        Point(pos.x, pos.y - 1),
        Point(pos.x, pos.y + 1),
        Point(pos.x - 1, pos.y),
        Point(pos.x + 1, pos.y),
    ]
    for neighbour in neighbours:
        is_in_bounds = 0 <= neighbour.x < width and 0 <= neighbour.y < height
        if not is_in_bounds:
            continue

        is_same_region = M[neighbour.y][neighbour.x] == M[pos.y][pos.x]
        if not is_same_region:
            continue

        is_unvisited = neighbour in unvisited
        if not is_unvisited:
            continue

        follow_region(M, neighbour, region, unvisited)


def determine_perimeter_part2(
        M: dict[int, dict[int, str]], region: list[Point]) -> int:
    perimeter = 0

    # Find all valid edges for each square in the region, storing them in
    # separate mappings of edge line X/Y positions to a list all squares
    # representing that edge
    left_edges_by_x: dict[int, list[Point]] = defaultdict(list)
    right_edges_by_x: dict[int, list[Point]] = defaultdict(list)
    top_edges_by_y: dict[int, list[Point]] = defaultdict(list)
    bottom_edges_by_y: dict[int, list[Point]] = defaultdict(list)

    width, height = len(M[0]), len(M)

    for p in region:
        left_is_edge = (p.x == 0) or (M[p.y][p.x] != M[p.y][p.x - 1])
        right_is_edge = (p.x == width-1) or (M[p.y][p.x] != M[p.y][p.x + 1])
        top_is_edge = (p.y == 0) or (M[p.y][p.x] != M[p.y - 1][p.x])
        bottom_is_edge = (p.y == height-1) or (M[p.y][p.x] != M[p.y + 1][p.x])

        if left_is_edge:
            left_edges_by_x[p.x].append(p)
        if right_is_edge:
            right_edges_by_x[p.x].append(p)
        if top_is_edge:
            top_edges_by_y[p.y].append(p)
        if bottom_is_edge:
            bottom_edges_by_y[p.y].append(p)

    # With squares comprising each edge grouped by their line position, we can
    # sort the grouped squares by their X or Y (using the Y value for left and
    # right edges and the X value for top and bottom edges). The sorted list
    # now gives us all the points comprising an edge in a line, with gaps in
    # the X or Y position (for top/bottom and left/right edges respectively)
    # indicating disconnected edges that count separately towards the
    # perimeter.
    # Each new group always adds one to the perimeter (as it represents a new
    # edge) and then any non-adjacent squares each add one to the perimeter as
    # these are disconnected edges.
    for _, points in left_edges_by_x.items():
        perimeter += 1
        points_sorted_by_y = sorted(points, key=lambda p: p.y)
        for p1, p2 in zip(points_sorted_by_y, points_sorted_by_y[1:]):
            if p2.y != p1.y + 1:
                perimeter += 1

    for _, points in right_edges_by_x.items():
        perimeter += 1
        points_sorted_by_y = sorted(points, key=lambda p: p.y)
        for p1, p2 in zip(points_sorted_by_y, points_sorted_by_y[1:]):
            if p2.y != p1.y + 1:
                perimeter += 1

    for _, points in top_edges_by_y.items():
        perimeter += 1
        points_sorted_by_x = sorted(points, key=lambda p: p.x)
        for p1, p2 in zip(points_sorted_by_x, points_sorted_by_x[1:]):
            if p2.x != p1.x + 1:
                perimeter += 1

    for _, points in bottom_edges_by_y.items():
        perimeter += 1
        points_sorted_by_x = sorted(points, key=lambda p: p.x)
        for p1, p2 in zip(points_sorted_by_x, points_sorted_by_x[1:]):
            if p2.x != p1.x + 1:
                perimeter += 1

    return perimeter


def part1(input: str) -> int:
    M: dict[int, dict[int, str]] = defaultdict(dict)

    unvisited: set[Point] = set()

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            M[y][x] = char
            unvisited.add(Point(x, y))

    width, height = x+1, y+1

    regions: list[list[Point]] = list()

    for y in range(height):
        for x in range(width):
            if (p := Point(x, y)) in unvisited:
                region: list[Point] = list()
                follow_region(M, p, region, unvisited)
                regions.append(region)

    total = 0
    for _, region in enumerate(regions):
        area = len(region)
        perimeter = 0
        for pos in region:
            neighbours = [
                Point(pos.x, pos.y - 1),
                Point(pos.x, pos.y + 1),
                Point(pos.x - 1, pos.y),
                Point(pos.x + 1, pos.y),
            ]
            for n in neighbours:
                # Inside the map, adjacent region must be different
                if 0 <= n.x < width and 0 <= n.y < height:
                    if M[n.y][n.x] != M[pos.y][pos.x]:
                        perimeter += 1
                # Outside thhe map, always counts
                else:
                    perimeter += 1
        total += area * perimeter

    return total


def part2(input: str) -> int:
    M: dict[int, dict[int, str]] = defaultdict(dict)

    unvisited: set[Point] = set()

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            M[y][x] = char
            unvisited.add(Point(x, y))

    width, height = x + 1, y + 1

    regions: list[list[Point]] = list()

    for y in range(height):
        for x in range(width):
            if (p := Point(x, y)) in unvisited:
                region: list[Point] = list()
                follow_region(M, p, region, unvisited)
                regions.append(region)

    total = 0
    for _, region in enumerate(regions):
        area = len(region)
        perimeter = determine_perimeter_part2(M, region)
        total += area * perimeter

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day12_example1.txt", part1, 140),
        ("Part 1", "inputs/day12_example2.txt", part1, 772),
        ("Part 1", "inputs/day12_example3.txt", part1, 1930),
        ("Part 1", "inputs/day12_full.txt", part1, 1424006),
        # Part 2 examples in the same order as the puzzle description
        ("Part 2", "inputs/day12_example1.txt", part2, 80),
        ("Part 2", "inputs/day12_example2.txt", part2, 436),
        ("Part 2", "inputs/day12_example4.txt", part2, 236),
        ("Part 2", "inputs/day12_example5.txt", part2, 368),
        ("Part 2", "inputs/day12_example3.txt", part2, 1206),
        ("Part 2", "inputs/day12_full.txt", part2, 858684),
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
