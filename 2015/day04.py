from hashlib import md5
from pathlib import Path
from time import time

YEAR = 2015
DAY = 4
NAME = "The Ideal Stocking Stuffer"


def solve(input: str, prefix: str) -> int:
    n = 0
    while True:
        key = input.strip() + str(n)
        h = md5(key.encode("utf-8"))
        if h.hexdigest().startswith(prefix):
            break
        n += 1
    return n


def part1(input: str) -> int:
    return solve(input, "00000")


def part2(input: str) -> int:
    return solve(input, "000000")


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day04_full.txt", part1, 282749),
        ("Part 2", "inputs/day04_full.txt", part2, 9962624)
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
