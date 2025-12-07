from functools import cache
from pathlib import Path
from time import time

YEAR = 2025
DAY = 7
NAME = "Laboratories"


def part1(input: str) -> int:
    total_splits = 0

    lines = input.strip().split("\n")

    start_pos = lines[0].find("S")
    active_beams: set[int] = set([start_pos])

    for line in lines[1:]:
        splitters = [i for i, c in enumerate(line) if c == "^"]

        if len(splitters) == 0:
            continue

        num_splits = 0
        split_beams: set[int] = set()
        for s in splitters:
            # Found a splitter, but it MUST have a beam going in.
            if s in active_beams:
                num_splits += 1
                if s-1 not in active_beams:
                    split_beams.add(s-1)
                if s+1 not in active_beams:
                    split_beams.add(s+1)

        active_beams.update(split_beams)

        # Splitters stop active beams so remove from the active set AFTER
        # updating the active beam set
        for s in splitters:
            if s in active_beams:
                active_beams.remove(s)

        total_splits += num_splits

    return total_splits


def part2(input: str) -> int:
    @cache
    def count_timelines(row: int, x: int) -> int:
        if row < len(lines) - 1:
            if lines[row][x] == "^":
                return (
                    count_timelines(row+1, x-1)
                    + count_timelines(row+1, x+1)
                )
            else:
                return count_timelines(row+1, x)
        else:
            return 1

    lines = input.strip().split("\n")
    start_pos = lines[0].find("S")
    result = count_timelines(1, start_pos)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day07_example.txt", part1, 21),
        ("Part 1", "inputs/day07_full.txt", part1, 1681),
        ("Part 2", "inputs/day07_example.txt", part2, 40),
        ("Part 2", "inputs/day07_full.txt", part2, 422102272495018),
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
