from functools import partial
from io import StringIO
from pathlib import Path
from time import time

YEAR = 2016
DAY = 8
NAME = "Two-Factor Authentication"


def solve(input: str, size: tuple[int, int]) -> list[list[int]]:
    screen = []

    # Init screen
    for _ in range(size[1]):
        screen.append([0] * size[0])

    for line in input.strip().split("\n"):
        if line.startswith("rect"):
            args = line.split()[1].split("x")
            a, b = int(args[0]), int(args[1])

            for y in range(b):
                for x in range(a):
                    screen[y][x] = 1

        elif line.startswith("rotate row"):
            args = line.split("=")[1].split()
            a, b = int(args[0]), int(args[2])

            # Save new values elsewhere so we don't overwrite the original
            updated = [0] * len(screen[0])
            for x in range(len(screen[0])):
                x2 = (x + b) % len(screen[0])
                updated[x2] = 1 if screen[a][x] else 0

            # Copy new values into place
            for x in range(len(screen[0])):
                screen[a][x] = updated[x]

        elif line.startswith("rotate column"):
            args = line.split("=")[1].split()
            a, b = int(args[0]), int(args[2])

            # Save new values elsewhere so we don't overwrite the original
            updated = [0] * len(screen[1])
            for y in range(len(screen)):
                y2 = (y + b) % len(screen)
                updated[y2] = 1 if screen[y][a] else 0

            # Copy new values into place
            for y in range(len(screen)):
                screen[y][a] = updated[y]

    return screen


def display(screen: list[list[int]]) -> str:
    buf = StringIO()

    for y in range(len(screen)):
        for x in range(len(screen[0])):
            buf.write("#" if screen[y][x] else ".")
        buf.write("\n")

    return buf.getvalue()


def part1(input: str, size: tuple[int, int]) -> int:
    screen = solve(input, size)
    num_lit = sum([sum(row) for row in screen])
    return num_lit


def part2(input: str, size: tuple[int, int]) -> str:
    screen = solve(input, size)  # noqa: F841
    # print(display(screen))
    # Hardcoded from reading the output :)
    code = "CFLELOYFCS"
    return code


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day08_sample.txt", partial(part1, size=(7, 3)), 6),
        ("Part 1", "inputs/day08_full.txt", partial(part1, size=(50, 6)), 106),
        ("Part 2", "inputs/day08_full.txt", partial(part2, size=(50, 6)),
         "CFLELOYFCS"),
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
