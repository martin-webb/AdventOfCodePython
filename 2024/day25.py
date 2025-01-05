from itertools import product
from time import time

DAY = 25
NAME = "Code Chronicle"


def part1(input: str) -> int:
    locks: list[tuple[int, ...]] = list()
    keys: list[tuple[int, ...]] = list()

    for block in input.strip().split("\n\n"):
        rows = block.split("\n")

        is_lock = (rows[0] == "#" * len(rows[0]))
        is_key = (rows[-1] == "#" * len(rows[-1]))
        assert is_lock or is_key

        heights = [0] * len(rows[0])
        for y in range(1, 6):
            for x in range(5):
                heights[x] += 1 if rows[y][x] == "#" else 0

        if is_lock:
            locks.append(tuple(heights))
        elif is_key:
            keys.append(tuple(heights))

    num_fit = 0

    for lock, key in product(locks, keys):
        if all([l + k <= 5 for l, k in zip(lock, key)]):
            num_fit += 1

    return num_fit


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day25_example.txt", part1, 3),
        ("Part 1", "inputs/day25_full.txt", part1, 3021),
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
