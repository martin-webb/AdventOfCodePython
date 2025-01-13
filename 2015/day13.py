from itertools import permutations
from pathlib import Path
from time import time

YEAR = 2015
DAY = 13
NAME = "Knights of the Dinner Table"


def parse_line(line: str) -> tuple[str, str, int]:
    parts = line.split()
    person_a, person_b = parts[0], parts[-1].strip(".")

    assert parts[2] in ("gain", "lose")

    if parts[2] == "gain":
        happiness = int(parts[3])
    elif parts[2] == "lose":
        happiness = -int(parts[3])

    return person_a, person_b, happiness


def max_happiness(P: set[str], H: dict[tuple[str, str], int]) -> int:
    max_happiness = float("-inf")

    for group in permutations(P, len(P)):
        h = 0
        for i in range(len(group)):
            j = (i + 1) % len(group)
            k = (i - 1) % len(group)
            h += H[(group[i], group[j])] + H[(group[i], group[k])]
        max_happiness = max(max_happiness, h)

    return int(max_happiness)


def part1(input: str) -> int:
    P: set[str] = set()  # People
    H: dict[tuple[str, str], int] = dict()  # Changes in happiness

    for line in input.strip().split("\n"):
        a, b, cost = parse_line(line)
        P.add(a)
        P.add(b)
        H[(a, b)] = cost

    result = max_happiness(P, H)
    return result


def part2(input: str) -> int:
    P: set[str] = set()  # People
    H: dict[tuple[str, str], int] = dict()  # Changes in happiness

    for line in input.strip().split("\n"):
        a, b, cost = parse_line(line)
        P.add(a)
        P.add(b)
        H[(a, b)] = cost

    me = "Me"
    P.add(me)
    for p in P:
        H[(me, p)] = 0
        H[(p, me)] = 0

    result = max_happiness(P, H)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day13_example.txt", part1, 330),
        ("Part 1", "inputs/day13_full.txt", part1, 618),
        ("Part 2", "inputs/day13_full.txt", part2, 601)
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
