from pathlib import Path
from time import time

YEAR = 2016
DAY = 2
NAME = "Bathroom Security"


def part1(input: str) -> str:
    KEYPAD = (
        ("1", "2", "3"),
        ("4", "5", "6"),
        ("7", "8", "9"),
    )
    MIN_X, MIN_Y, MAX_X, MAX_Y = 0, 0, len(KEYPAD)-1, len(KEYPAD)-1

    code = ""

    position = (1, 1)
    for line in input.strip().split("\n"):
        for c in line:
            if c == "U":
                position = (position[0], max(position[1]-1, MIN_Y))
            elif c == "D":
                position = (position[0], min(position[1]+1, MAX_Y))
            elif c == "L":
                position = (max(position[0]-1, MIN_X), position[1])
            elif c == "R":
                position = (min(position[0]+1, MAX_X), position[1])

        button = KEYPAD[position[1]][position[0]]
        code += button

    return code


def part2(input: str) -> str:
    KEYPAD = (
        (None, None, "1", None, None),
        (None, "2",  "3", "4", None),
        ("5",  "6",  "7", "8", "9"),
        (None, "A",  "B", "C", None),
        (None, None, "D", None, None),
    )
    MIN_X, MIN_Y, MAX_X, MAX_Y = 0, 0, len(KEYPAD)-1, len(KEYPAD)-1

    code = ""

    position = (0, 2)
    for line in input.strip().split("\n"):
        for c in line:
            if c == "U":
                next_position = (position[0], max(position[1]-1, MIN_Y))
            elif c == "D":
                next_position = (position[0], min(position[1]+1, MAX_Y))
            elif c == "L":
                next_position = (max(position[0]-1, MIN_X), position[1])
            elif c == "R":
                next_position = (min(position[0]+1, MAX_X), position[1])

            if KEYPAD[next_position[1]][next_position[0]] is not None:
                position = next_position

        button = KEYPAD[position[1]][position[0]]
        assert button is not None
        code += button

    return code


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day02_sample.txt", part1, "1985"),
        ("Part 1", "inputs/day02_full.txt", part1, "92435"),
        ("Part 2", "inputs/day02_sample.txt", part2, "5DB3"),
        ("Part 2", "inputs/day02_full.txt", part2, "C1A88"),
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
