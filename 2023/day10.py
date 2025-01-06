from copy import copy
from pathlib import Path
from time import time

YEAR = 2023
DAY = 10
NAME = "Pipe Maze"


def nextdirection(pos: tuple[int, int],
                  prev: tuple[int, int],
                  pipe: str) -> tuple[int, int]:
    """
    >>> nextdirection((1, 1), (1, 0), '|') # from: above, to: below
    (1, 2)
    >>> nextdirection((1, 1), (1, 2), '|') # from: below, to: above
    (1, 0)
    >>> nextdirection((1, 1), (0, 1), '-') # from: left, to: right
    (2, 1)
    >>> nextdirection((1, 1), (2, 1), '-') # from: right, to: left
    (0, 1)
    >>> nextdirection((1, 1), (1, 0), 'L') # from: above, to: right
    (2, 1)
    >>> nextdirection((1, 1), (2, 1), 'L') # from: right, to: above
    (1, 0)
    >>> nextdirection((1, 1), (1, 0), 'J') # from: above, to: left
    (0, 1)
    >>> nextdirection((1, 1), (0, 1), 'J') # from: left, to: above
    (1, 0)
    >>> nextdirection((1, 1), (0, 1), '7') # from: left, to: below
    (1, 2)
    >>> nextdirection((1, 1), (1, 2), '7') # from: below, to: left
    (0, 1)
    >>> nextdirection((1, 1), (2, 1), 'F') # from: right, to: below
    (1, 2)
    >>> nextdirection((1, 1), (1, 2), 'F') # from: below, to: right
    (2, 1)
    """
    if pipe == "|":
        return (pos[0], pos[1]+1) if pos[1] > prev[1] else (pos[0], pos[1]-1)
    elif pipe == "-":
        return (pos[0]+1, pos[1]) if pos[0] > prev[0] else (pos[0]-1, pos[1])
    elif pipe == "L":
        return (pos[0]+1, pos[1]) if pos[1] > prev[1] else (pos[0], pos[1]-1)
    elif pipe == "J":
        return (pos[0]-1, pos[1]) if prev[1] < pos[1] else (pos[0], pos[1]-1)
    elif pipe == "7":
        return (pos[0], pos[1]+1) if prev[0] < pos[0] else (pos[0]-1, pos[1])
    elif pipe == "F":
        return (pos[0], pos[1]+1) if prev[0] > pos[0] else (pos[0]+1, pos[1])
    else:
        raise RuntimeError(f"Asked direction for non-pipe tile '{pipe}'")


def startnext(loc: tuple[int, int],
              grid: list[list[str]]) -> list[tuple[int, int]]:
    """
    Returns the next two positions from the given start position ('S') going in
    each direction.
    """
    n = []

    # North
    if loc[1]-1 >= 0 and grid[loc[1]-1][loc[0]] in ("|", "F", "7"):
        n.append((loc[0], loc[1] - 1))

    # South
    if loc[1]+1 < len(grid) and grid[loc[1]+1][loc[0]] in ("|", "J", "L"):
        n.append((loc[0], loc[1] + 1))

    # East
    if loc[0]+1 < len(grid[0]) and grid[loc[1]][loc[0]+1] in ("-", "7", "J"):
        n.append((loc[0] + 1, loc[1]))

    # West
    if loc[0]-1 >= 0 and grid[loc[1]][loc[0]-1] in ("-", "L", "F"):
        n.append((loc[0] - 1, loc[1]))

    return n


def direction_from_positions(a: tuple[int, int], b: tuple[int, int]) -> str:
    """
    Direction of travel to get from position a to position b.
    >>> direction_from_positions((0, 0), (1, 0))
    'RIGHT'
    >>> direction_from_positions((1, 0), (0, 0))
    'LEFT'
    >>> direction_from_positions((0, 0), (0, 1))
    'DOWN'
    >>> direction_from_positions((0, 1), (0, 0))
    'UP'
    >>> direction_from_positions((0, 0), (0, 0))
    Traceback (most recent call last):
        ...
    AssertionError: Positions are the same
    >>> direction_from_positions((0, 0), (1, 1))
    Traceback (most recent call last):
        ...
    AssertionError: Positions not adjacent in one direction ((0, 0), (1, 1))
    """
    assert a != b, "Positions are the same"
    assert (
        (a[0] == b[0] and a[1] != b[1]) or (a[0] != b[0] and a[1] == b[1])
    ), f"Positions not adjacent in one direction ({a}, {b})"

    if b[0] > a[0]:
        return "RIGHT"
    elif b[0] < a[0]:
        return "LEFT"
    elif b[1] > a[1]:
        return "DOWN"
    elif b[1] < a[1]:
        return "UP"
    raise RuntimeError("Couldn't determine direction from position")


def next_turn(cur: tuple[int, int],
              prev: tuple[int, int],
              grid: list[list[str]]) -> tuple[tuple[int, int], str]:
    """
    2-tuple position of the next turn on from the current position, following
    the direction established by the previous position.
    """
    c = copy(cur)
    p = copy(prev)
    while True:
        n = nextdirection(c, p, grid[c[1]][c[0]])
        p, c = c, n
        t = grid[c[1]][c[0]]
        if direction_from_positions(p, c) == "UP" and t in ("7", "F"):
            return c, t
        elif direction_from_positions(p, c) == "DOWN" and t in ("J", "L"):
            return c, t
        elif direction_from_positions(p, c) == "LEFT" and t in ("L", "F"):
            return c, t
        elif direction_from_positions(p, c) == "RIGHT" and t in ("7", "J"):
            return c, t

    raise RuntimeError(
        f"Failed to determine next turn (current={cur}, previous={prev})")


def s_to_turn(
        s: tuple[int, int], a: tuple[int, int], b: tuple[int, int]) -> str:
    """
    >>> s_to_turn((10, 10), (11, 10), (9, 10))
    '-'
    >>> s_to_turn((10, 10), (10, 11), (10, 9))
    '|'
    >>> s_to_turn((10, 10), (9, 10), (10, 9))
    'J'
    >>> s_to_turn((10, 10), (10, 9), (11, 10))
    'L'
    >>> s_to_turn((10, 10), (9, 10), (10, 11))
    '7'
    >>> s_to_turn((10, 10), (10, 11), (11, 10))
    'F'
    """
    # Sort the neighbouring positions first so we can compare with a and b
    # passed in any order
    aa, bb = sorted([a, b])
    if s == (aa[0]+1, aa[1]) and s == (bb[0]-1, bb[1]):
        return "-"
    if s == (aa[0], aa[1]+1) and s == (bb[0], bb[1]-1):
        return "|"
    if s == (aa[0]+1, aa[1]) and s == (bb[0], bb[1]+1):
        return "J"
    if s == (aa[0], aa[1]+1) and s == (bb[0]-1, bb[1]):
        return "L"
    if s == (aa[0]+1, aa[1]) and s == (bb[0], bb[1]-1):
        return "7"
    if s == (aa[0], aa[1]-1) and s == (bb[0]-1, bb[1]):
        return "F"
    raise RuntimeError(
        f"Couldn't determine type of S (spos={s}, n1={aa}, n2={bb})")


def part1(input: str) -> int:
    lines = input.strip().split("\n")

    grid = []
    sloc = None
    for y, line in enumerate(lines):
        row = list(line)
        if (sidx := line.find("S")) != -1:
            sloc = (sidx, y)
        grid.append(row)

    assert sloc is not None

    loc = copy(sloc)
    current = startnext(sloc, grid)
    prevs = [loc, loc]
    distance = 1  # We've already moved one step by finding the first next locs
    while True:
        nexts = [
            nextdirection(current[i],
                          prevs[i],
                          grid[current[i][1]][current[i][0]])
            for i in range(len(current))
        ]
        prevs = list(current)
        current = nexts
        distance += 1

        if current[0] == current[1]:
            break

    return distance


def part2(input: str) -> int:
    lines = input.strip().split("\n")

    # First need to find all the positions that are actually in the loop
    grid = []
    sloc = None
    for y, line in enumerate(lines):
        row = list(line)
        if (sidx := line.find("S")) != -1:
            sloc = (sidx, y)
        grid.append(row)

    assert sloc is not None

    loc = copy(sloc)
    starts = startnext(sloc, grid)
    current = starts[0]
    prev = copy(sloc)
    positions = set([loc])
    while True:
        tile = grid[current[1]][current[0]]
        if tile == "S":
            break
        positions.add(current)
        next = nextdirection(current, prev, tile)
        current, prev = next, current

    assert sloc is not None
    stype = s_to_turn(sloc, starts[0], starts[1])

    num_inside = 0
    for y, line in enumerate(lines):
        # Replace S with its actual type as implied by its two neighbours
        if "S" in line:
            line = line.replace("S", stype)

        is_inside = False
        last_y = 0

        for x in range(len(line)):
            ctype = line[x]
            cpos = (x, y)

            # "|", "F" and "L" are always state flips
            # "J" and "7" are conditional state flips that require a previous
            # turn with the same vertical direction in order to count as a flip
            if cpos in positions:
                if ctype == "|":
                    is_inside = not is_inside
                elif ctype == "F":
                    is_inside = not is_inside
                    last_y = 1
                elif ctype == "L":
                    is_inside = not is_inside
                    last_y = -1
                elif ctype == "J":
                    if last_y == -1:
                        is_inside = not is_inside
                    last_y = -1
                elif ctype == "7":
                    if last_y == 1:
                        is_inside = not is_inside
                    last_y = 1

            if is_inside and cpos not in positions:
                num_inside += 1

    return num_inside


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day10_part1_example1.txt", part1, 4),
        ("Part 1", "inputs/day10_part1_example2.txt", part1, 8),
        ("Part 1", "inputs/day10_full.txt", part1, 6882),
        ("Part 2", "inputs/day10_part2_example1.txt", part2, 4),
        ("Part 2", "inputs/day10_part2_example2.txt", part2, 4),
        ("Part 2", "inputs/day10_part2_example3.txt", part2, 8),
        ("Part 2", "inputs/day10_part2_example4.txt", part2, 10),
        ("Part 2", "inputs/day10_full.txt", part2, 491),
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
