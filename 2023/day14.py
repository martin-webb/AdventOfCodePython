from collections import Counter
from dataclasses import dataclass
from functools import cache
from time import time
from typing import Optional

DAY = 14
NAME = "Parabolic Reflector Dish"


@dataclass
class CycleBoundary:
    pos: int
    spin: Optional[tuple[str, ...]]


@cache
def transpose(rows: tuple[str]) -> tuple[str, ...]:
    """
    >>> transpose(('AB', 'CD'))
    ('AC', 'BD')
    >>> transpose(transpose(('AB', 'CD')))
    ('AB', 'CD')
    """
    return tuple(
        [
            "".join(rows[y][x] for y in range(len(rows)))
            for x in range(len(rows[0]))
        ]
    )


@cache
def slide_subsection(s: str) -> str:
    """
    >>> slide_subsection('OO.O.O..')
    'OOOO....'
    """
    return ("O" * s.count("O")) + ("." * s.count("."))


@cache
def slide_up(cols: tuple[str]) -> tuple[str, ...]:
    """
    >>> slide_up(('..O..#..O', '....OOOO'))
    ('O....#O..', 'OOOO....')
    """
    return tuple(
        [
            "#".join([slide_subsection(c) for c in col.split("#")])
            for col in cols
        ]
    )


@cache
def rotate_ccw(cols: tuple[str]) -> tuple[str, ...]:
    """
    >>> rotate_ccw(('ABCD', 'EFGH', 'IJKL'))
    ('DHL', 'CGK', 'BFJ', 'AEI')
    """
    rows = []
    for x in range(len(cols[0]) - 1, -1, -1):
        row = ""
        for y in range(len(cols)):
            row += cols[y][x]
        rows.append(row)
    return tuple(rows)


@cache
def spin_cycle(cols: tuple[str, ...]) -> tuple[str, ...]:
    """
    A spin cycle involves slides north, west, south and east, however we can
    simply rotate the grid and use the slide north from Part 1 on the rotated
    grid.
    """
    cols = slide_up(cols)
    cols = rotate_ccw(cols)
    cols = slide_up(cols)
    cols = rotate_ccw(cols)
    cols = slide_up(cols)
    cols = rotate_ccw(cols)
    cols = slide_up(cols)
    cols = rotate_ccw(cols)
    return cols


def part1(input: str) -> int:
    rows = tuple([line for line in input.split("\n") if line != ""])
    cols = transpose(rows)

    cols_slided = slide_up(cols)
    rows_slided = transpose(cols_slided)

    load = sum(
        [row.count("O") * (len(rows_slided) - i)
         for i, row in enumerate(rows_slided)]
    )
    return load


def part2(input: str) -> int:
    rows = tuple([line for line in input.split("\n") if line != ""])
    cols = transpose(rows)

    hash_counts = Counter()  # type: ignore[var-annotated]
    cycle_begin: Optional[CycleBoundary] = None
    cycle_end: Optional[CycleBoundary] = None

    last_spin = None
    spun = tuple(cols)
    # Let's hope we can find a cycle before 1,000,000,000 iterations...
    for i in range(1_000_000_000):
        spun = spin_cycle(spun)
        spin_hash = hash(spun)
        hash_counts[spin_hash] += 1

        if hash_counts[spin_hash] >= 3 and cycle_end is None:
            cycle_end = CycleBoundary(pos=i - 1, spin=last_spin)
        elif hash_counts[spin_hash] >= 2 and cycle_begin is None:
            cycle_begin = CycleBoundary(pos=i - 1, spin=last_spin)

        last_spin = spun

        if cycle_begin is not None and cycle_end is not None:
            break

    assert cycle_begin is not None
    assert cycle_end is not None

    num_unrepeated = cycle_begin.pos + 1
    cycle_length = cycle_end.pos - cycle_begin.pos
    remaining_spins = (1_000_000_000 - num_unrepeated) % cycle_length

    assert cycle_end.spin is not None

    spun = cycle_end.spin
    for i in range(remaining_spins):
        spun = spin_cycle(spun)

    rows_slided = transpose(spun)

    load = sum(
        [row.count("O") * (len(rows_slided) - i)
         for i, row in enumerate(rows_slided)]
    )

    return load


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day14_example.txt", part1, 136),
        ("Part 1", "inputs/day14_full.txt", part1, 108955),
        ("Part 2", "inputs/day14_example.txt", part2, 64),
        ("Part 2", "inputs/day14_full.txt", part2, 106689),
    ):
        with open(filename) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
