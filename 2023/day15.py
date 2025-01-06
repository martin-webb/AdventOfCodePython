from collections import defaultdict
from pathlib import Path
from time import time

YEAR = 2023
DAY = 15
NAME = "Lens Library"


def HASH(s: str) -> int:
    value = 0

    for char in s:
        value += ord(char)
        value *= 17
        value %= 256

    return value


def process_lens_equals(lenses: list[tuple[str, int]],
                        new: tuple[str, int]) -> list[tuple[str, int]]:
    for i in range(len(lenses)):
        if lenses[i][0] == new[0]:
            lenses[i] = new
            break
    else:
        lenses.append(new)

    return lenses


def process_lens_dash(lenses: list[tuple[str, int]],
                      label: str) -> list[tuple[str, int]]:
    for i in range(len(lenses)):
        if lenses[i][0] == label:
            del lenses[i]
            break

    return lenses


def part1(input: str) -> int:
    sum = 0

    for x in input.strip().split(","):
        sum += HASH(x)

    return sum


def part2(input: str) -> int:
    sum = 0

    boxes_to_lenses = defaultdict(list)  # type: ignore[var-annotated]

    for token in input.strip().split(","):
        if "=" in token:
            label, focal_length = (x := token.split("="), x[0], int(x[1]))[1:]
            box = HASH(label)
            boxes_to_lenses[box] = process_lens_equals(boxes_to_lenses[box],
                                                       (label, focal_length))
        elif "-" in token:
            label = token.split("-")[0]
            box = HASH(label)
            boxes_to_lenses[box] = process_lens_dash(boxes_to_lenses[box],
                                                     label)
            if len(boxes_to_lenses[box]) == 0:
                del boxes_to_lenses[box]

    for k, lenses in boxes_to_lenses.items():
        for i, lens in enumerate(lenses):
            value = (int(k) + 1) * (i + 1) * lens[1]
            sum += value

    return sum


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day15_example.txt", part1, 1320),
        ("Part 1", "inputs/day15_full.txt", part1, 506891),
        ("Part 2", "inputs/day15_example.txt", part2, 145),
        ("Part 2", "inputs/day15_full.txt", part2, 230462),
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
