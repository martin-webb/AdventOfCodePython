from pathlib import Path
from time import time

YEAR = 2025
DAY = 4
NAME = "Printing Department"


def parse_input(input: str) -> dict[tuple[int, int], str]:
    grid: dict[tuple[int, int], str] = dict()

    lines = input.strip().split("\n")
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x, y)] = c

    return grid


def count_removals(grid: dict[tuple[int, int], str], repeated: bool) -> int:
    total = 0

    directions = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0),           (1, 0),
        (-1, 1),  (0, 1),  (1, 1)
    ]

    # Inclusive
    x_max = max(k[0] for k in grid.keys())
    y_max = max(k[1] for k in grid.keys())

    while True:
        num_removed = 0

        # Copy the current state so we can update this for a possible next
        # iteration while counting the unmodified original
        # Used for part 2 with iterated remove passes
        updated_grid: dict[tuple[int, int], str] = dict(grid)

        for y in range(y_max+1):
            for x in range(x_max+1):
                if grid[(x, y)] != "@":
                    continue

                neighbours = [(x+d[0], y+d[1]) for d in directions]
                num_adjacent = 0

                for neighbour in neighbours:
                    if neighbour not in grid:
                        continue
                    if grid[neighbour] == "@":
                        num_adjacent += 1

                if num_adjacent < 4:
                    updated_grid[(x, y)] = "."
                    num_removed += 1

        grid = updated_grid
        total += num_removed

        if repeated:
            if num_removed == 0:
                break
        else:
            break

    return total


def part1(input: str) -> int:
    grid = parse_input(input)
    result = count_removals(grid, False)
    return result


def part2(input: str) -> int:
    grid = parse_input(input)
    result = count_removals(grid, True)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day04_example.txt", part1, 13),
        ("Part 1", "inputs/day04_full.txt", part1, 1486),
        ("Part 2", "inputs/day04_example.txt", part2, 43),
        ("Part 2", "inputs/day04_full.txt", part2, 9024),
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
