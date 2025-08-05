from functools import partial
from pathlib import Path
from time import time

YEAR = 2016
DAY = 18
NAME = "Like a Rogue"

TRAPS = set(["^^.", ".^^", "^..", "..^"])


def solve(input: str, rows: int) -> int:
    num_safe = 0

    # Pad with implicitly safe tiles at the edges (count -2 later for padding)
    row = "." + input.strip() + "."
    num_safe += row.count(".") - 2

    for _ in range(rows - 1):
        row = "." + "".join([
            "^" if row[x-1:x+2] in TRAPS else "." for x in range(1, len(row)-1)
        ]) + "."
        num_safe += row.count(".") - 2

    return num_safe


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day18_example.txt",
         partial(solve, rows=10), 38),
        ("Part 1", "inputs/day18_full.txt",
         partial(solve, rows=40), 1939),
        ("Part 2", "inputs/day18_full.txt",
         partial(solve, rows=400000), 19999535),
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
