from hashlib import md5
from pathlib import Path
from time import time
from typing import Optional

YEAR = 2016
DAY = 5
NAME = "How About a Nice Game of Chess?"

VALID_POSITIONS = set("01234567")


def part1(input: str) -> str:
    password = ""

    door_id = input.strip()

    n = -1  # First iteration will be 0
    while True:
        n += 1

        h = md5(f"{door_id}{n}".encode("utf-8"))
        digest = h.hexdigest()
        if digest[:5] == "00000":
            password += digest[5]

        if len(password) == 8:
            break

    return password


def part2(input: str) -> str:
    values: list[Optional[str]] = [None] * 8

    door_id = input.strip()

    n = -1  # First iteration will be 0
    while True:
        n += 1

        h = md5(f"{door_id}{n}".encode("utf-8"))
        digest = h.hexdigest()

        if digest[:5] == "00000":
            pos, char = digest[5], digest[6]

            if pos not in VALID_POSITIONS:
                continue

            # Use only the first character found for any given position
            if values[int(pos)] is not None:
                continue

            values[int(pos)] = char

            if all(values):
                break

    password = "".join([v for v in values if v is not None])
    return password


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day05_full.txt", part1, "f97c354d"),
        ("Part 2", "inputs/day05_full.txt", part2, "863dde27"),
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
