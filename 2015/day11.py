from pathlib import Path
import re
import string
from time import time

YEAR = 2015
DAY = 11
NAME = "Corporate Policy"

CHARS = string.ascii_lowercase.translate({
    ord("i"): (""),
    ord("l"): (""),
    ord("o"): ("")
})


def increment_password(pw: str) -> str:
    for i in range(len(pw) - 1, -1, -1):
        if pw[i] == "z":
            pw = pw[:i] + "a" + pw[i+1:]
        else:
            pw = pw[:i] + CHARS[CHARS.index(pw[i]) + 1] + pw[i+1:]
            break
    return pw


def is_password_valid(pw: str) -> bool:
    """
    NOTE: Rules evaluated in the order that generally discards
    naively incremented password as soon as possible.
    """
    # Rule 3: Two different non-overlapping pairs
    pairs = set(re.findall(r'(.)\1', pw))
    if len(pairs) < 2:
        return False

    # Rule 1: Increasing straights of three
    for i in range(len(pw) - 2):
        a, b, c = pw[i], pw[i + 1], pw[i + 2]
        a_pos, b_pos, c_pos = CHARS.index(a), CHARS.index(b), CHARS.index(c)
        if a_pos == b_pos - 1 and b_pos == c_pos - 1:
            break
    else:
        return False

    # Rule 2: No confusing letters
    if re.search(r'iol', pw):
        return False

    return True


def next_password(pw: str) -> str:
    while True:
        pw = increment_password(pw)
        if is_password_valid(pw):
            return pw


def part1(input: str) -> str:
    password = input.strip()
    return next_password(password)


def part2(input: str) -> str:
    password = input.strip()
    return next_password(next_password(password))


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day11_full.txt", part1, "cqjxxyzz"),
        ("Part 2", "inputs/day11_full.txt", part2, "cqkaabcc")
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
