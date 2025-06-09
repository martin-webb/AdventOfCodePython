from pathlib import Path
import re
from string import ascii_lowercase
from time import time

YEAR = 2016
DAY = 7
NAME = "Internet Protocol Version 7"


def part1(input: str) -> int:
    count = 0

    ABBA_COMBINATIONS = [f"{a}{b}{b}{a}"
                         for a in ascii_lowercase
                         for b in ascii_lowercase
                         if a != b]
    ABBA_PATTERN = "|".join(ABBA_COMBINATIONS)

    for line in input.strip().split("\n"):
        # Substitute out the hypernet sequences to get the supernets
        # We keep a single space as the replacement to allow us to match
        # against a single string without overlapping separate sequences
        supernets = re.sub(r"\[[a-z]+\]", " ", line)

        # Extract the hypernet sequences, again keeping separate sequences
        # separated by a single space to allow matching against a single string
        # without overlapping separate sequences
        hypernets = " ".join(re.findall(r"\[([a-z]+)\]", line))

        abba_in_supernets = re.search(ABBA_PATTERN, supernets)
        abba_in_hypernets = re.search(ABBA_PATTERN, hypernets)

        if abba_in_supernets is not None and abba_in_hypernets is None:
            count += 1

    return count


def part2(input: str) -> int:
    count = 0

    ABA_COMBINATIONS = [f"{a}{b}{a}"
                        for a in ascii_lowercase
                        for b in ascii_lowercase
                        if a != b]
    ABA_ALTERNATION = "|".join(ABA_COMBINATIONS)

    # NOTE: Lookahead assertion to allow e.g. zaz|zbz zazbz to both match
    ABA_PATTERN = fr"(?=({ABA_ALTERNATION}))"

    for line in input.strip().split("\n"):
        # Substitute out the hypernet sequences to get the supernets
        # We keep a single space as the replacement to allow us to match
        # against a single string without overlapping separate sequences
        supernets = re.sub(r"\[[a-z]+\]", " ", line)

        # Extract the hypernet sequences, again keeping separate sequences
        # separated by a single space to allow matching against a single string
        # without overlapping separate sequences
        hypernets = " ".join(re.findall(r"\[([a-z]+)\]", line))

        abas = re.findall(ABA_PATTERN, supernets)
        for aba in abas:
            bab = f"{aba[1]}{aba[0]}{aba[1]}"
            bab_in_hypernets = re.search(bab, hypernets)
            if bab_in_hypernets is not None:
                count += 1
                break

    return count


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day07_part1_sample.txt", part1, 2),
        ("Part 1", "inputs/day07_full.txt", part1, 115),
        ("Part 2", "inputs/day07_part2_sample.txt", part2, 3),
        ("Part 2", "inputs/day07_full.txt", part2, 231),
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
