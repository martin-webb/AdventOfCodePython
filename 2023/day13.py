from pathlib import Path
from time import time
from typing import Generator, Optional

YEAR = 2023
DAY = 13
NAME = "Point of Incidence"


def transpose(pattern: list[str]) -> list[str]:
    """
    >>> transpose([
    ...     "..##..##.",
    ...     "..#.##.#.",
    ...     "##......#",
    ...     "##......#",
    ...     "..#.##.#.",
    ...     "..##..##.",
    ...     "#.#.##.#."
    ... ])
    ['..##..#', '..##...', '##..###', '#....#.', '.#..#.#', '.#..#.#', '#....#.', '##..###', '..##...']  # noqa: E501
    """
    transposed = ["".join([pattern[y][x]
                  for y in range(len(pattern))])
                  for x in range(len(pattern[0]))
                  ]
    return transposed


def find_symmetry(
        pattern: list[str], exclusions: Optional[set[int]] = None) -> int:
    # Exclusions set added for Part 2.
    # This is a set of values we don't consider as valid symmetries to return.
    # A nicer looking solution would be to always support returning ALL
    # symmetries we find (and filtering out unwanted ones in the caller), but
    # this way requires less adjustment to the calling code and this can still
    # be used in Part 1 like this.
    # NOTE: Although we're using a set here we only expect there to be a single
    # value and in the Part 2 implementation we only pass in a single-valued
    # set.
    # Default value as None due to default mutable arguments behaviour.
    if exclusions is None:
        exclusions = set()

    ymax = len(pattern) - 1

    for b in range(1, len(pattern)):
        a = b - 1
        row_a = pattern[a]
        row_b = pattern[b]

        if row_a != row_b:
            continue

        for i in range(1, min(a, ymax - b) + 1):
            assert (a - i >= 0) and (b + i < len(pattern))
            row_aa = pattern[a - i]
            row_bb = pattern[b + i]
            if row_aa != row_bb:
                break
        else:
            symmetry = a + 1
            if symmetry not in exclusions:
                return symmetry

    return 0


def smudged(pattern: list[str]) -> Generator[list[str], None, None]:
    """
    >>> list(smudged(['..', '..']))
    [['#.', '..'], ['.#', '..'], ['..', '#.'], ['..', '.#']]
    """
    for y, line in enumerate(pattern):
        for x, char in enumerate(line):
            if char == ".":
                char2 = "#"
            else:
                char2 = "."
            line2 = line[:x] + char2 + line[x+1:]
            pattern2 = []
            pattern2 += pattern[:y]
            pattern2.append(line2)
            pattern2 += pattern[y+1:]
            yield pattern2


def part1(input: str) -> int:
    lines = input.split("\n")

    patterns = []
    current_pattern: list[str] = []
    for line in lines:
        # Empty rows separate pattern lines
        if line.strip() == "":
            patterns.append(current_pattern)
            current_pattern = list()
        else:
            current_pattern.append(line)

    sum = 0

    for pattern in patterns:
        h = find_symmetry(pattern)
        transposed = transpose(pattern)
        v = find_symmetry(transposed)
        sum += v
        sum += h * 100

    return sum


def part2(input: str) -> int:
    lines = input.split("\n")

    patterns = []
    current_pattern: list[str] = []
    for line in lines:
        # Empty rows separate pattern lines
        if line.strip() == "":
            patterns.append(current_pattern)
            current_pattern = list()
        else:
            current_pattern.append(line)

    sum = 0

    for pattern in patterns:
        original_h = find_symmetry(pattern)
        original_v = find_symmetry(transpose(pattern))

        updated_v = original_v
        updated_h = original_h

        for smudge_pattern in smudged(pattern):
            smudged_h = find_symmetry(smudge_pattern,
                                      set([original_h]))
            smudged_v = find_symmetry(transpose(smudge_pattern),
                                      set([original_v]))

            if smudged_v != 0:
                updated_v = smudged_v
            if smudged_h != 0:
                updated_h = smudged_h

        if original_v != updated_v:
            sum += updated_v
        if original_h != updated_h:
            sum += updated_h * 100

    return sum


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day13_example.txt", part1, 405),
        ("Part 1", "inputs/day13_custom1.txt", part1, 709),
        ("Part 1", "inputs/day13_full.txt", part1, 33780),
        ("Part 2", "inputs/day13_example.txt", part2, 400),
        ("Part 2", "inputs/day13_custom1.txt", part2, 1400),
        ("Part 2", "inputs/day13_full.txt", part2, 23479),
    ):

        path = Path(__file__).parent / filename
        with open(path) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
