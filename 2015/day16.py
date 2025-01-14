from pathlib import Path
from time import time

YEAR = 2015
DAY = 16
NAME = "Aunt Sue"

REFERENCE = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1
}


def parse_line(line: str) -> tuple[int, dict]:
    name, compounds_s = line.split(": ", 1)
    sue = int(name.split()[1])
    compounds = {}
    for compound_s in compounds_s.split(", "):
        name, value = compound_s.split(": ")
        compounds[name] = int(value)
    return sue, compounds


def part1(input: str) -> int:
    scores: dict[int, int] = dict()
    for line in input.strip().split("\n"):
        sue, compounds = parse_line(line)
        difference = 0
        for name, compound_ref in REFERENCE.items():
            if name in compounds:
                difference += abs(compound_ref - compounds[name])
        scores[sue] = difference

    sorted_scores = sorted(scores.items(), key=lambda item: item[1])
    sue = sorted_scores[0][0]
    return sue


def part2(input: str) -> int:
    scores: dict[int, int] = dict()
    for line in input.strip().split("\n"):
        num, compounds = parse_line(line)
        difference = 0
        for name, compound_ref in REFERENCE.items():
            if name in compounds:
                if name in ("cats", "trees"):
                    difference += 0 if compounds[name] > compound_ref else 1
                elif name in ("pomeranians", "goldfish"):
                    difference += 0 if compounds[name] < compound_ref else 1
                else:
                    difference += abs(compound_ref - compounds[name])
        scores[num] = difference

    sorted_scores = sorted(scores.items(), key=lambda item: item[1])
    sue = sorted_scores[0][0]
    return sue


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day16_full.txt", part1, 213),
        ("Part 1", "inputs/day16_full.txt", part2, 323)
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
