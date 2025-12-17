from collections import deque
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Optional

YEAR = 2025
DAY = 12
NAME = "Christmas Tree Farm"

SHAPE_LENGTH_MAX = 3

Pattern3x3 = tuple[int, int, int]
Grid = tuple[int, ...]


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Shape:
    index: int
    patterns: tuple[Pattern3x3]

    def num_blocks(self) -> int:
        # All rotations have the same block count so we can use any pattern
        return sum(n.bit_count() for n in self.patterns[0])


@dataclass(frozen=True)
class Region:
    width: int
    height: int
    shape_requirements: tuple[int, ...]


QueueEntry = tuple[Point, tuple[int, ...], list[int], int, int]


def parse_pattern(lines: list[str]) -> Pattern3x3:
    """
    >>> parse_pattern(["###", "##.", "##."])
    (7, 6, 6)
    >>> parse_pattern([".#.", "###", "###"])
    (2, 7, 7)
    """
    assert len(lines) == 3
    assert all(len(s) == 3 for s in lines)

    # Row-major numbering
    p11 = ((1 << 2) if lines[0][0] == "#" else 0)
    p12 = ((1 << 1) if lines[0][1] == "#" else 0)
    p13 = ((1 << 0) if lines[0][2] == "#" else 0)

    p21 = ((1 << 2) if lines[1][0] == "#" else 0)
    p22 = ((1 << 1) if lines[1][1] == "#" else 0)
    p23 = ((1 << 0) if lines[1][2] == "#" else 0)

    p31 = ((1 << 2) if lines[2][0] == "#" else 0)
    p32 = ((1 << 1) if lines[2][1] == "#" else 0)
    p33 = ((1 << 0) if lines[2][2] == "#" else 0)

    pattern: Pattern3x3 = (
         p11 | p12 | p13,
         p21 | p22 | p23,
         p31 | p32 | p33
    )
    return pattern


def rotate_pattern_cw(pattern: Pattern3x3) -> Pattern3x3:
    """
    >>> rotate_pattern_cw((0b111, 0b110, 0b110))
    (7, 7, 1)
    >>> rotate_pattern_cw((0b010, 0b111, 0b111))
    (6, 7, 6)
    """
    # Square shapes fixed for puzzle inputs so use that here for simplicity

    p11 = (pattern[2] & (1 << 2))
    p12 = (pattern[1] & (1 << 2)) >> 1
    p13 = (pattern[0] & (1 << 2)) >> 2

    p21 = (pattern[2] & (1 << 1)) << 1
    p22 = (pattern[1] & (1 << 1))
    p23 = (pattern[0] & (1 << 1)) >> 1

    p31 = (pattern[2] & (1 << 0)) << 2
    p32 = (pattern[1] & (1 << 0)) << 1
    p33 = (pattern[0] & (1 << 0))

    rotated: Pattern3x3 = (
        p11 | p12 | p13,
        p21 | p22 | p23,
        p31 | p32 | p33
    )
    return rotated


def deduplicate_patterns(patterns: tuple[Pattern3x3]) -> tuple[Pattern3x3]:
    """
    De-deuplicates rotationally symmetric patterns.
    """
    deduplicated: tuple[Pattern3x3] = ()

    seen: set[Pattern3x3] = set()
    for pattern in patterns:
        if pattern not in seen:
            deduplicated += (pattern,)

            # Not technically needed for the last one but also no real need to
            # make this conditional
            seen.add(pattern)

    return deduplicated


def parse_input(text: str) -> tuple[dict[int, Shape], list[Region]]:
    shapes: dict[int, Shape] = dict()
    regions: list[Region] = list()

    sections = text.strip().split("\n\n")

    shape_blocks = sections[:-1]
    for shape_block in shape_blocks:
        shape_lines = shape_block.split("\n")
        index_line = shape_lines[0]
        index = int(index_line.strip(":"))

        # The number suffix is notionally the 'rotation', but we don't really
        # need that information here or later, we simply use this here to show
        # that we do 3 x 90 degree rotations on each previous pattern to get
        # the full set of candidates
        pattern_0 = parse_pattern(shape_lines[1:])
        pattern_90 = rotate_pattern_cw(pattern_0)
        pattern_180 = rotate_pattern_cw(pattern_90)
        pattern_270 = rotate_pattern_cw(pattern_180)

        candidates = (
            pattern_0, pattern_90, pattern_180, pattern_270
        )
        patterns = deduplicate_patterns(candidates)

        shape = Shape(index, patterns)
        shapes[index] = shape

    regions_block = sections[-1]
    for line in regions_block.split("\n"):
        area, index_requirements_line = line.split(":")
        width, height = [int(n) for n in area.split("x")]
        requirements = tuple(int(n) for n in index_requirements_line.split())
        region = Region(width, height, requirements)
        regions.append(region)

    return (shapes, regions)


def shape_fits(src: Point, pattern: Pattern3x3, grid: Grid) -> bool:
    """
    >>> shape_fits(Point(0, 0), (0b111, 0b111, 0b111), (0b0, 0b0, 0b0))
    True
    >>> shape_fits(Point(0, 0), (0b111, 0b101, 0b101), (0b0, 0b010, 0b010))
    True
    >>> shape_fits(Point(0, 0), (0b111, 0b101, 0b101), (0b100, 0b000, 0b000))
    False
    >>> shape_fits(Point(0, 0), (0b001, 0b001, 0b001), (0b000, 0b000, 0b001))
    False
    """
    for i in range(SHAPE_LENGTH_MAX):
        g = (grid[src.y + i] >> src.x) & 0b111
        if g & pattern[i] != 0:
            return False
    return True


def next_point(region: Region, grid: Grid, curpos: Point) -> Optional[Point]:
    """
    >>> next_point(Region(4, 4, ()), ([0b0, 0b0, 0b0, 0b0]), Point(0, 0))
    Point(x=0, y=1)
    >>> next_point(Region(4, 4, ()), ([0b1, 0b1, 0b0, 0b0]), Point(0, 1))
    Point(x=1, y=0)
    >>> next_point(Region(4, 4, ()), ([0b11, 0b11, 0b11, 0b11]), Point(1, 3))
    """
    has_vertical_space = (curpos.y + 1) <= (region.height - SHAPE_LENGTH_MAX)
    has_horizontal_space = (curpos.x + 1) <= (region.width - SHAPE_LENGTH_MAX)

    if has_vertical_space:
        return Point(curpos.x, curpos.y + 1)  # Move down
    elif has_horizontal_space:
        return Point(curpos.x + 1, 0)  # Move along and reset y
    else:
        return None


def place_pattern_in_grid(pattern: Pattern3x3, grid: Grid, src: Point) -> Grid:
    """
    >>> place_pattern_in_grid((0b111, 0b101, 0b111), (0, 0, 0), Point(0, 0))
    (7, 5, 7)
    """
    copied = list(grid)

    for i in range(SHAPE_LENGTH_MAX):
        # Safety/consistency (can use original or copied here)
        # NOTE: Row-by-row, so don't need to worry about partial updates
        assert (((grid[src.y + i] >> src.x) & 0b111) & pattern[i]) == 0
        copied[src.y + i] |= (pattern[i] << src.x)

    return tuple(copied)


def next_nonzero_index(l: list[int]) -> int:
    for i, n in enumerate(l):
        if n != 0:
            return i
    return -1


def can_fit(region: Region, shapes: dict[int, Shape]) -> bool:
    """
    """
    result = False

    # Testing with fill grid, might be able to use vertical slices
    # XXX: Grid grows with (0, 0) as LSB for simplicity (auto bignum promotion
    # in Python, no circular shift/rotate without pre-determined max width)
    first: QueueEntry = (
        Point(0, 0),
        tuple([0] * region.height),
        list(region.shape_requirements),
        sum(region.shape_requirements),
        0
    )

    Q: deque[QueueEntry] = deque([first])
    while Q:
        src, grid, remaining, remaining_total, depth = Q.pop()

        if remaining_total == 0:
            result = True
            break
        else:
            # Scan down the frontier, testing shape inverses for
            # Perhaps rank by spikyness or awkwardness of the left edge
            # We can check against a small pre-baked template for this?
            nextpos = next_point(region, grid, src)
            if nextpos is None:
                continue

            # The final option option is to just move our placement position
            # without having places a polyomino
            # XXX: Pushed FIRST so it runs LAST (LIFO)
            Q.append((nextpos, grid, remaining, remaining_total, depth+1))

            shape_idx = next_nonzero_index(remaining)
            shape = shapes[shape_idx]

            for pattern in shape.patterns:
                if shape_fits(src, pattern, grid):
                    copied = place_pattern_in_grid(pattern, grid, src)
                    updated_remaining = list(remaining)
                    updated_remaining[shape_idx] -= 1
                    child = (
                        nextpos,
                        copied,
                        updated_remaining,
                        remaining_total-1,
                        depth+1
                    )
                    Q.append(child)

    return result


def part1(text: str) -> int:
    shapes, regions = parse_input(text)

    num_possible = 0
    for region in regions:
        area_available = region.width * region.height
        area_required = 0
        for i, n in enumerate(region.shape_requirements):
            shape = shapes[i]
            area_required += shape.num_blocks() * n

        # Ignore if there"s physically not enough space (no overlap allowed)
        if area_required > area_available:
            continue

        if can_fit(region, shapes):
            num_possible += 1

    return num_possible


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day12_example.txt", part1, 2),
        ("Part 1", "inputs/day12_full.txt", part1, 567),
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
