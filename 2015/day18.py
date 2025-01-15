from pathlib import Path
from time import time

YEAR = 2015
DAY = 18
NAME = "Like a GIF For Your Yard"


def simulate(
    lights: dict[tuple[int, int], int],
    x_max: int,
    y_max: int,
    iters: int,
    always_on: set[tuple[int, int]]
) -> dict[tuple[int, int], int]:
    neighbours = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0),           (1, 0),
        (-1, 1),  (0, 1),  (1, 1),
    ]
    for _ in range(iters):
        updated: dict[tuple[int, int], int] = dict()
        for y in range(y_max):
            for x in range(x_max):
                neighbours_lit = sum(
                    [lights.get((x+n[0], y+n[1]), 0) for n in neighbours]
                )
                if (x, y) in always_on:
                    updated[(x, y)] = 1
                else:
                    if lights[(x, y)] == 1:
                        updated[(x, y)] = 1 if neighbours_lit in (2, 3) else 0
                    else:
                        updated[(x, y)] = 1 if neighbours_lit == 3 else 0
        lights = updated
    return lights


def part1(input: str) -> int:
    lights: dict[tuple[int, int], int] = dict()

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            lights[(x, y)] = 1 if char == "#" else 0

    x_max, y_max = x + 1, y + 1

    lights = simulate(lights, x_max, y_max, 100, set())

    lights_on = sum(lights.values())
    return lights_on


def part2(input: str) -> int:
    lights: dict[tuple[int, int], int] = dict()

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            lights[(x, y)] = 1 if char == "#" else 0

    x_max, y_max = x + 1, y + 1

    stuck_on = {(0, 0), (x_max-1, 0), (0, y_max-1), (x_max-1, y_max-1)}
    for s in stuck_on:
        lights[s] = 1

    lights = simulate(lights, x_max, y_max, 100, stuck_on)

    lights_on = sum(lights.values())
    return lights_on


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day18_full.txt", part1, 814),
        ("Part 2", "inputs/day18_full.txt", part2, 924),
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
