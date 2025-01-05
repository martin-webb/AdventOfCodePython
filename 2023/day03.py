from collections import Counter, defaultdict
from dataclasses import dataclass, field
from time import time
from typing import Generator

YEAR = 2023
DAY = 3
NAME = "Gear Ratios"


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


@dataclass
class SchematicNumber:
    x: int
    y: int
    digits: str
    is_part: bool

    # Part 2 only (safe to leave this here for Part 1)
    adjacent_gears: set = field(default_factory=set)


def neighbours(x: int,
               y: int,
               radius: int,
               x_min: int,
               x_max: int,
               y_min: int,
               y_max: int) -> Generator[tuple[int, int], None, None]:
    x_min = max(x - radius, x_min)
    x_max = min(x + radius, x_max)
    y_min = max(y - radius, y_min)
    y_max = min(y + radius, y_max)

    for yy in range(y_min, y_max + 1):
        for xx in range(x_min, x_max + 1):
            if xx == x and yy == y:  # Neighbours only
                continue
            yield (xx, yy)


def is_surrounded_by_symbol(grid: list[list[str]], x: int, y: int) -> bool:
    for xx, yy in neighbours(x, y, 1, 0, len(grid[0]) - 1, 0, len(grid) - 1):
        c = grid[yy][xx]
        if not c.isdigit() and c != ".":
            return True
    return False


def adjacent_gears(grid: list[list[str]], x: int, y: int) -> set[Point]:
    gears = set()

    for xx, yy in neighbours(x, y, 1, 0, len(grid[0]) - 1, 0, len(grid) - 1):
        if grid[yy][xx] == "*":
            gear = Point(xx, yy)
            gears.add(gear)

    return gears


def part1(input: str) -> int:
    part_sum = 0

    grid = []
    for line in input.strip().split("\n"):
        grid.append(list(line))

    width = len(grid[0])
    height = len(grid)

    schematics = []

    for y in range(height):
        current_schematic = None
        for x in range(width):
            char = grid[y][x]
            if char.isdigit():
                if current_schematic is None:
                    current_schematic = SchematicNumber(
                        x=x,
                        y=y,
                        digits=char,
                        is_part=False
                    )
                else:
                    current_schematic.digits += char

                if is_surrounded_by_symbol(grid, x, y):
                    current_schematic.is_part = True
            else:
                if current_schematic is not None:
                    schematics.append(current_schematic)
                    current_schematic = None

            # End any current schematic number at the end of an input line
            if x == width - 1:
                if current_schematic is not None:
                    schematics.append(current_schematic)
                    current_schematic = None

    for schematic in schematics:
        if schematic.is_part:
            part_sum += int(schematic.digits)

    return part_sum


def part2(input: str) -> int:
    gear_ratio_sum = 0

    grid = []
    for line in input.strip().split("\n"):
        grid.append(list(line))

    width = len(grid[0])
    height = len(grid)

    schematics = []

    for y in range(height):
        current_schematic = None
        for x in range(width):
            char = grid[y][x]
            if char.isdigit():
                if current_schematic is None:
                    current_schematic = SchematicNumber(
                        x=x,
                        y=y,
                        digits=char,
                        is_part=False
                    )
                else:
                    current_schematic.digits += char

                if is_surrounded_by_symbol(grid, x, y):
                    current_schematic.is_part = True

                adj_gears = adjacent_gears(grid, x, y)
                for ag in adj_gears:
                    current_schematic.adjacent_gears.add(ag)
            else:
                if current_schematic is not None:
                    schematics.append(current_schematic)
                    current_schematic = None

            # End any current schematic number at the end of an input line
            if x == width - 1:
                if current_schematic is not None:
                    schematics.append(current_schematic)
                    current_schematic = None

    gear_references = Counter()  # type: ignore[var-annotated]
    for schematic in schematics:
        for gear in schematic.adjacent_gears:
            gear_references[gear] += 1

    actual_gears = set(
        gear for gear, count in gear_references.items() if count == 2
    )

    gears_to_parts = defaultdict(list)
    for schematic in schematics:
        for gear in schematic.adjacent_gears:
            gears_to_parts[gear].append(schematic)

    for gear in actual_gears:
        total = 1
        for part in gears_to_parts[gear]:
            total *= int(part.digits)
        gear_ratio_sum += total

    return gear_ratio_sum


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day03_example.txt", part1, 4361),
        ("Part 1", "inputs/day03_full.txt", part1, 549908),
        ("Part 2", "inputs/day03_example.txt", part2, 467835),
        ("Part 2", "inputs/day03_full.txt", part2, 81166799),
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
