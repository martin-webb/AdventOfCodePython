from functools import partial
from io import StringIO
from pathlib import Path
from time import time

YEAR = 2016
DAY = 16
NAME = "Dragon Checksum"


def step(a: str) -> str:
    """
    >>> step("1")
    '100'
    >>> step("0")
    '001'
    >>> step("11111")
    '11111000000'
    >>> step("111100001010")
    '1111000010100101011110000'
    """
    trans = str.maketrans({"0": "1", "1": "0"})
    b = a[::-1]
    b = b.translate(trans)
    return a + "0" + b


def checksum(a: str) -> str:
    assert len(a) % 2 == 0, "Input to checksum length not even"

    checksum = a

    while True:
        buf = StringIO()
        for i in range(0, len(checksum), 2):
            ab = checksum[i:i+2]
            if ab == "11" or ab == "00":
                buf.write("1")
            else:
                buf.write("0")

        checksum = buf.getvalue()
        if len(checksum) % 2 == 0:
            continue
        else:
            break

    return checksum


def solve(input: str, length: int) -> str:
    """
    Simple iterated solution that runs fast enough for both parts.
    TODO: Revisit this to investigate any optimisation based on the reference
    to the dragon curve in the puzzle description.
    """
    a = input.strip()
    while len(a) < length:
        a = step(a)
    a = a[:length]
    chk = checksum(a)
    return chk


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day16_example.txt",
         partial(solve, length=20), "01100"),
        ("Part 1", "inputs/day16_full.txt",
         partial(solve, length=272), "01110011101111011"),
        ("Part 2", "inputs/day16_full.txt",
         partial(solve, length=35651584), "11001111011000111"),
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
