from collections import Counter
from functools import partial
from pathlib import Path
from time import time

YEAR = 2015
DAY = 14
NAME = "Reindeer Olympics"


def parse_input(input: str) -> list[tuple[str, int, int, int]]:
    reindeer: list[tuple[str, int, int, int]] = list()

    for line in input.strip().split("\n"):
        parts = line.split()
        name = parts[0]
        speed = int(parts[3])
        fly_secs = int(parts[6])
        rest_secs = int(parts[13])
        reindeer.append((name, speed, fly_secs, rest_secs))

    return reindeer


def part1(input: str, secs: int) -> int:
    reindeer = parse_input(input)

    max_distance = float("-inf")

    for _, speed, fly_secs, rest_secs in reindeer:
        cycles = secs // (fly_secs + rest_secs)
        remaining = secs % (fly_secs + rest_secs)
        distance = \
            (cycles * speed * fly_secs) + (speed * min(remaining, fly_secs))
        max_distance = max(max_distance, distance)

    return int(max_distance)


def part2(input: str, secs: int) -> int:
    reindeer = parse_input(input)

    points: Counter[str] = Counter()
    distances: Counter[str] = Counter()

    for n in range(secs):
        for r in reindeer:
            name, speed, fly_secs, rest_secs = r
            remaining = n % (fly_secs + rest_secs)
            distances[name] += speed if remaining < fly_secs else 0

        winning = max(distances.values())
        for name, distance in distances.items():
            if distance == winning:
                points[name] += 1

    winning_points = points.most_common()[0][1]
    return winning_points


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day14_example.txt",
         partial(part1, secs=1000), 1120),
        ("Part 1", "inputs/day14_full.txt",
         partial(part1, secs=2503), 2655),
        ("Part 1", "inputs/day14_example.txt",
         partial(part2, secs=1000), 689),
        ("Part 2", "inputs/day14_full.txt",
         partial(part2, secs=2503), 1059)
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
