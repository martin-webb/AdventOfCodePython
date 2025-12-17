from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from time import perf_counter

YEAR = 2025
DAY = 9
NAME = "Movie Theater"


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True, order=True)
class Rect:
    src: Point  # Inclusive
    dst: Point  # Inclusive

    def __post_init__(self) -> None:
        if self.src.x > self.dst.x or self.src.y > self.dst.y:
            raise ValueError(f"Rect corners not normalized: {self}")

    def overlaps(self, other: "Rect") -> bool:
        # Strict interior overlap (no touching)
        return not (
            self.dst.x <= other.src.x or
            other.dst.x <= self.src.x or
            self.dst.y <= other.src.y or
            other.dst.y <= self.src.y
        )

    def area(self) -> int:
        return (self.dst.x - self.src.x + 1) * (self.dst.y - self.src.y + 1)


def parse_input(text: str) -> list[Point]:
    points: list[Point] = []

    for line in text.strip().split("\n"):
        x, y = [int(n) for n in line.split(",")]
        points.append(Point(x, y))

    # Puzzle input consistency
    n = len(points)
    assert all(
        (points[i].x == points[(i+1) % n].x)
        ^ (points[i].y == points[(i+1) % n].y)
        for i in range(n)
    ), "Expected consecutive vertices with same-x xor same-y"

    return points


def find_vertex_turns(points: list[Point]) -> list[int]:
    turns: list[int] = []

    for i in range(len(points)):
        a = points[i-1]
        b = points[i]
        c = points[(i+1) % len(points)]
        abx, aby = b.x - a.x, b.y - a.y
        bcx, bcy = c.x - b.x, c.y - b.y
        turns.append(abx * bcy - aby * bcx)

    return turns


def find_forbidden_rects_from_concave_vertices(
        points: list[Point], turns: list[int]) -> list[Rect]:
    rects: list[Rect] = []

    for i in range(len(points)):
        turn = turns[i]

        # Assumes input vertices are in CW order with y increasing downward
        if turn < 0:
            pa = points[i-1]
            pb = points[i]
            pc = points[(i+1) % len(points)]

            # Make top-left and bottom-right
            x1 = min(pa.x, pb.x, pc.x)
            x2 = max(pa.x, pb.x, pc.x)
            y1 = min(pa.y, pb.y, pc.y)
            y2 = max(pa.y, pb.y, pc.y)

            # The convex/concave corner defines a forbidden *outside* bite
            # We shrink by 1 so rectangles that merely touch the boundary
            # aren't rejected under strict interior overlap.
            rect = Rect(Point(x1, y1), Point(x2-1, y2-1))

            rects.append(rect)

    # Sort because after visualising the polygon we know that sorting by
    # largest area is a massive win for performance as this allows us to bail
    # out of the check-all as quickly as possible
    rects = sorted(rects, key=lambda r: r.area(), reverse=True)

    return rects


def part1(text: str) -> int:
    # Treat chosen red tiles as opposite corners of an axis-aligned rectangle
    points = parse_input(text)

    max_area = 0
    for p1, p2 in combinations(points, 2):
        xd = abs(p1.x - p2.x) + 1
        yd = abs(p1.y - p2.y) + 1
        area = xd * yd
        max_area = max(max_area, area)

    return max_area


def part2(text: str) -> int:
    # Treat chosen red tiles as opposite corners of an axis-aligned rectangle
    points = parse_input(text)

    turns = find_vertex_turns(points)
    forbidden_rects = find_forbidden_rects_from_concave_vertices(points, turns)

    max_area = 0

    for p1, p2 in combinations(points, 2):
        x1, x2 = p1.x, p2.x
        if x2 < x1:
            x1, x2 = x2, x1

        y1, y2 = p1.y, p2.y
        if y2 < y1:
            y1, y2 = y2, y1

        rect = Rect(Point(x1, y1), Point(x2, y2))

        if not any(rect.overlaps(c) for c in forbidden_rects):
            max_area = max(max_area, rect.area())

    return max_area


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day09_example.txt", part1, 50),
        ("Part 1", "inputs/day09_full.txt", part1, 4759531084),
        ("Part 2", "inputs/day09_example.txt", part2, 24),
        ("Part 2", "inputs/day09_full.txt", part2, 1539238860),
    ):
        path = Path(__file__).parent / filename
        with open(path) as f:
            contents = f.read()

        t1 = perf_counter()
        result = func(contents)
        t2 = perf_counter()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)",
              "\u2B50"
              if expected is not None
              and result == expected
              and "_full" in filename
              else "")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
