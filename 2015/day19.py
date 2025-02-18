from collections import defaultdict
from pathlib import Path
import re
from time import time

YEAR = 2015
DAY = 19
NAME = "Medicine for Rudolph"


def parse_input(input: str) -> tuple[dict[str, set[str]], str]:
    replacements_str, start = input.strip().split("\n\n")

    replacements: dict[str, set[str]] = defaultdict(set)
    for r in replacements_str.split("\n"):
        a, b = r.split(" => ")
        replacements[a].add(b)

    return replacements, start


def replace_once(s: str, replacements: dict[str, set[str]]) -> set[str]:
    molecules: set[str] = set()

    for k, V in replacements.items():
        for v in V:
            for match in re.finditer(k, s):
                s1 = s[:match.span()[0]]
                s2 = v
                s3 = s[match.span()[1]:]
                replaced = s1 + s2 + s3
                molecules.add(replaced)

    return molecules


def min_replacements_to_molecule(
    current: str,
    target: str,
    replacements: dict[str, str],
    total_steps: int = 0
) -> int:
    if current == target:
        return total_steps
    else:
        # Find all possible transformations for the current molecule using each
        # replacement as many times as possible consecutively, then use the
        # shortest resulting molecule as the next molecule to transform.
        # NOTE: This is completely input dependent and doesn't work on (for
        # example) the example in the puzzle description.
        transformations: list[tuple[str, int]] = list()
        for k, v in replacements.items():
            steps = current.count(k)
            if steps > 0:
                transformed = current.replace(k, v)
                transformations.append((transformed, steps))

        for transformed, steps in sorted(transformations,
                                         key=lambda item: len(item[0]),
                                         reverse=True):
            return min_replacements_to_molecule(
                transformed, target, replacements, total_steps+steps)

        return int(float("inf"))


def part1(input: str) -> int:
    replacements, start = parse_input(input)
    molecules = replace_once(start, replacements)
    return len(molecules)


def part2(input: str) -> int:
    replacements, start = parse_input(input)

    target = "e"

    replacements_reversed: dict[str, str] = dict()
    for k, V in replacements.items():
        for v in V:
            replacements_reversed[v] = k

    result = min_replacements_to_molecule(start, target, replacements_reversed)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day19_full.txt", part1, 576),
        ("Part 2", "inputs/day19_full.txt", part2, 207),
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
