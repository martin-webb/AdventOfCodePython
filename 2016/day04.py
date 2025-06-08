from collections import Counter
from dataclasses import dataclass
import re
from pathlib import Path
from time import time

YEAR = 2016
DAY = 4
NAME = "Security Through Obscurity"


@dataclass
class Room:
    name: str
    sector_id: int
    checksum_actual: str
    checksum_expected: str


def parse_room(s: str) -> Room:
    match = re.match(r"([a-z-]+)-([0-9]+)\[([a-z]+)\]", s)
    assert match is not None

    name = match.group(1)
    sector_id = int(match.group(2))
    checksum = match.group(3)

    name_letters = [c for c in name if c.isalpha()]
    name_letter_counts = Counter(name_letters)

    # Sorted by most common with ties broken by alphabetisation
    name_letters_sorted = sorted(name_letter_counts.most_common(),
                                 key=lambda item: (-item[1], item[0]))

    expected_checksum = "".join(x[0] for x in name_letters_sorted[:5])

    room = Room(
        name=name,
        sector_id=sector_id,
        checksum_actual=checksum,
        checksum_expected=expected_checksum
    )
    return room


def decrypt_name(encrypted: str, n: int) -> str:
    decrypted = ""

    for c in encrypted:
        if c.isalpha():
            o = ord(c) - ord("a")
            o2 = ((o + n) % 26) + ord("a")
            decrypted += chr(o2)
        else:
            decrypted += " "

    return decrypted


def part1(input: str) -> int:
    result = 0

    for line in input.strip().split("\n"):
        room = parse_room(line)

        if room.checksum_actual != room.checksum_expected:
            continue

        result += room.sector_id

    return result


def part2(input: str) -> int:
    result = None

    for line in input.strip().split("\n"):
        room = parse_room(line)

        # I'm not sure if we're only intended to decrypt non-decoy rooms but it
        # doesn't affect the answer in my input data
        if room.checksum_actual != room.checksum_expected:
            continue

        decrypted_name = decrypt_name(room.name, room.sector_id)
        if decrypted_name == "northpole object storage":
            result = room.sector_id
            break

    assert result is not None
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day04_sample.txt", part1, 1514),
        ("Part 1", "inputs/day04_full.txt", part1, 278221),
        ("Part 2", "inputs/day04_full.txt", part2, 267),
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
