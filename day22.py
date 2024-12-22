from collections import defaultdict, deque
from time import time

DAY = 22
NAME = "Monkey Market"


def mix(a: int, b: int) -> int:
    return a ^ b


def prune(a: int) -> int:
    return a % 16777216


def evolve(n: int) -> int:
    n = prune(mix(n * 64, n))
    n = prune(mix(int(n // 32), n))
    n = prune(mix(n * 2048, n))
    return n


def part1(input: str) -> int:
    total = 0

    for line in input.strip().split("\n"):
        secret = int(line)
        for _ in range(2000):
            secret = evolve(secret)
        total += secret

    return total


def part2(input: str) -> int:
    counts: dict[tuple, int] = defaultdict(int)

    for line in input.strip().split("\n"):
        secret = int(line)
        changes: deque[int] = deque(maxlen=4)
        seen = set()
        for _ in range(2000):
            next_secret = evolve(secret)
            change = (next_secret % 10) - (secret % 10)
            changes.append(change)
            if len(changes) == 4:
                sequence = tuple(changes)
                if sequence not in seen:
                    counts[sequence] += next_secret % 10
                    seen.add(sequence)
            secret = next_secret

    sorted_counts = sorted(counts.items(),
                           key=lambda item: item[1], reverse=True)
    return sorted_counts[0][1]


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day22_part1_example.txt", part1, 37327623),
        ("Part 1", "inputs/day22_full.txt", part1, 19458130434),
        ("Part 2", "inputs/day22_part2_example.txt", part2, 23),
        ("Part 2", "inputs/day22_full.txt", part2, 2130),
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
