from enum import Enum
from pathlib import Path
from time import time

YEAR = 2016
DAY = 9
NAME = "Explosives in Cyberspace"


class ParseState(Enum):
    OUTSIDE_MARKER = 0
    PARSING_MARKER_A = 1
    PARSING_MARKER_B = 2


def decompressed_length(s: str, version: int) -> int:
    length = 0

    state = ParseState.OUTSIDE_MARKER
    a = 0
    b = 0

    i = -1
    while True:
        i += 1

        if i >= len(s):
            break

        c = s[i]

        if state == ParseState.OUTSIDE_MARKER:
            if c == "(":
                state = ParseState.PARSING_MARKER_A
            else:
                length += 1

        elif state == ParseState.PARSING_MARKER_A:
            if c == "x":
                state = ParseState.PARSING_MARKER_B
            else:
                a = (a * 10) + int(c)

        elif state == ParseState.PARSING_MARKER_B:
            if c == ")":
                if version == 1:
                    length += a * b
                elif version == 2:
                    decompressed_section = s[i+1:i+1+a]
                    length += b * decompressed_length(decompressed_section,
                                                      version=version)
                else:
                    raise ValueError(
                        "Unexpected version, expected 1 or 2, got {version}")

                state = ParseState.OUTSIDE_MARKER
                i += a
                a = 0
                b = 0
            else:
                b = (b * 10) + int(c)

    return length


def part1(input: str) -> int:
    compressed = input.strip()
    length = decompressed_length(compressed, version=1)
    return length


def part2(input: str) -> int:
    compressed = input.strip()
    length = decompressed_length(compressed, version=2)
    return length


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day09_full.txt", part1, 150914),
        ("Part 2", "inputs/day09_full.txt", part2, 11052855125),
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
