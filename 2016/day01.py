from pathlib import Path
from time import time

YEAR = 2016
DAY = 1
NAME = "No Time for a Taxicab"


def part1(input: str) -> int:
    position = 0+0j
    direction = -1j

    instructions = input.strip().split(", ")
    for instruction in instructions:
        d, n = instruction[0], int(instruction[1:])
        if d == "R":
            direction *= 1j
        elif d == "L":
            direction *= -1j
        position += direction * n

    distance = abs(int(position.real)) + abs(int(position.imag))
    return distance


def part2(input: str) -> int:
    position = 0+0j
    direction = -1j

    visited = set()

    instructions = input.strip().split(", ")
    for instruction in instructions:
        d, n = instruction[0], int(instruction[1:])
        if d == "R":
            direction *= 1j
        elif d == "L":
            direction *= -1j

        for _ in range(n):
            position += direction
            if position in visited:
                break
            visited.add(position)
        else:
            continue

        break

    distance = abs(int(position.real)) + abs(int(position.imag))
    return distance


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day01_full.txt", part1, 273),
        ("Part 2", "inputs/day01_full.txt", part2, 115),
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
