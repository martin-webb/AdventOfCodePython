from collections import defaultdict
from io import StringIO
from dataclasses import dataclass
from functools import cache
from itertools import permutations
from pathlib import Path
from time import time

YEAR = 2024
DAY = 21
NAME = "Keypad Conundrum"


@dataclass(eq=True, frozen=True)
class Vec2i:
    x: int
    y: int

    def __add__(self, other: "Vec2i") -> "Vec2i":
        if not isinstance(other, Vec2i):
            raise TypeError(
                "__add__() argument must be a Vec2i, " +
                f"not {other.__class__.__name__}"
            )
        return Vec2i(self.x + other.x, self.y + other.y)


UP = Vec2i(0, -1)
DOWN = Vec2i(0, 1)
LEFT = Vec2i(-1, 0)
RIGHT = Vec2i(1, 0)


NUMPAD_POSITIONS = {
    "1": Vec2i(0, 2),
    "2": Vec2i(1, 2),
    "3": Vec2i(2, 2),
    "4": Vec2i(0, 1),
    "5": Vec2i(1, 1),
    "6": Vec2i(2, 1),
    "7": Vec2i(0, 0),
    "8": Vec2i(1, 0),
    "9": Vec2i(2, 0),
    "0": Vec2i(1, 3),
    "A": Vec2i(2, 3)
}

NUMPAD_POSITION_INVALID = Vec2i(0, 3)

KEYPAD_POSITIONS = {
    "^": Vec2i(1, 0),
    "v": Vec2i(1, 1),
    "<": Vec2i(0, 1),
    ">": Vec2i(2, 1),
    "A": Vec2i(2, 0)
}

KEYPAD_POSITION_INVALID = Vec2i(0, 0)


def numpad_movements(a: str, b: str) -> list[tuple[str, Vec2i]]:
    """
    Generate one potential movement from numpad key a to key b, returning a
    list of pairs of the individual movement as a string and the direction of
    that movement as an offset.
    The single movement generated here is one of a number of potential valid
    movements from key to a to key b that favours the fewest number of changes
    of direction, but doesn't include all possible ways of getting from key a
    to key b.
    """
    movements = list()

    src = NUMPAD_POSITIONS[a]
    dst = NUMPAD_POSITIONS[b]

    is_up = dst.y <= src.y  # less-than-or-equal to ensure we can go horizontal
    is_down = dst.y > src.y
    is_left = dst.x <= src.x  # less-than-or-equal to ensure we can go vertical
    is_right = dst.x > src.x

    if is_up and is_right:
        for _ in range(src.y, dst.y, -1):
            movements.append(("^", UP))
        for _ in range(src.x, dst.x):
            movements.append((">", RIGHT))

    elif is_up and is_left:
        for _ in range(src.y, dst.y, -1):
            movements.append(("^", UP))
        for _ in range(src.x, dst.x, -1):
            movements.append(("<", LEFT))

    elif is_down and is_right:
        for _ in range(src.y, dst.y):
            movements.append(("v", DOWN))
        for _ in range(src.x, dst.x):
            movements.append((">", RIGHT))

    elif is_down and is_left:
        for _ in range(src.y, dst.y):
            movements.append(("v", DOWN))
        for _ in range(src.x, dst.x, -1):
            movements.append(("<", LEFT))

    return movements


def keypad_movements(a: str, b: str) -> list[tuple[str, Vec2i]]:
    """
    Generate one potential movement from keypad key a to key b, returning a
    list of pairs of the individual movement as a string and the direction of
    that movement as an offset.
    The single movement generated here is one of a number of potential valid
    movements from key to a to key b that favours the fewest number of changes
    of direction, but doesn't include all possible ways of getting from key a
    to key b.
    """
    movements: list[tuple[str, Vec2i]] = list()

    src = KEYPAD_POSITIONS[a]
    dst = KEYPAD_POSITIONS[b]

    is_up = dst.y <= src.y  # less-than-or-equal to ensure we can go horizontal
    is_down = dst.y > src.y
    is_left = dst.x <= src.x  # less-than-or-equal to ensure we can go vertical
    is_right = dst.x > src.x

    if is_up and is_right:
        for _ in range(src.y, dst.y, -1):
            movements.append(("^", UP))
        for _ in range(src.x, dst.x):
            movements.append((">", RIGHT))

    elif is_up and is_left:
        for _ in range(src.y, dst.y, -1):
            movements.append(("^", UP))
        for _ in range(src.x, dst.x, -1):
            movements.append(("<", LEFT))

    elif is_down and is_right:
        for _ in range(src.y, dst.y):
            movements.append(("v", DOWN))
        for _ in range(src.x, dst.x):
            movements.append((">", RIGHT))

    elif is_down and is_left:
        for _ in range(src.y, dst.y):
            movements.append(("v", DOWN))
        for _ in range(src.x, dst.x, -1):
            movements.append(("<", LEFT))

    return movements


@cache
def numpad_movement_permutations(a: str, b: str) -> set[str]:
    """
    Generate all possible valid movements from numpad key a to key b, ignoring
    any invalid movements (ones that pass over the gap in the numpad) and
    returning a set of unique movement strings that represent the buttons to be
    pressed to get from key a to key b (and to actually press key b).
    """
    movements: set[str] = set()

    start_position = NUMPAD_POSITIONS[a]
    for movements_permutation in permutations(numpad_movements(a, b)):
        s = StringIO()
        invalid = False
        position = start_position
        for movement in movements_permutation:
            position += movement[1]
            if position == NUMPAD_POSITION_INVALID:
                invalid = True
                break

            s.write(movement[0])

        if invalid:
            continue

        s.write("A")  # Has to end with an A to trigger the action
        movements.add(s.getvalue())

    return movements


@cache
def keypad_movement_permutations(a: str, b: str) -> set[str]:
    """
    Generate all possible valid movements from keypad key a to key b, ignoring
    any invalid movements (ones that pass over the gap in the numpad) and
    returning a set of unique movement strings that represent the buttons to be
    pressed to get from key a to key b (and to actually press key b).
    """
    movements: set[str] = set()

    start_position = KEYPAD_POSITIONS[a]
    for movements_permutation in permutations(keypad_movements(a, b)):
        s = StringIO()
        invalid = False
        position = start_position
        for movement in movements_permutation:
            position += movement[1]
            if position == KEYPAD_POSITION_INVALID:
                invalid = True
                break

            s.write(movement[0])

        if invalid:
            continue

        s.write("A")
        movements.add(s.getvalue())

    return movements


@cache
def shortest_length(
    a: str,
    b: str,
    max_depth: int,
    depth: int = 0
) -> tuple[int, str]:
    """
    Compute the global shortest length from key a to key b, including both
    numpad key presses and keypad key presses, taking into account the given
    number of intermediate keypads.
    """
    total = 0

    if depth == 0:
        counts: dict[int, int] = defaultdict(int)
        for i, movement in enumerate(numpad_movement_permutations(a, b)):
            p0 = "A"
            for p1 in movement:
                subtotal, p0 = shortest_length(p0, p1, max_depth, depth+1)
                counts[i] += subtotal
        total += min(counts.values())

    elif depth > 0 and depth < max_depth:
        counts: dict[int, int] = defaultdict(int)  # type: ignore[no-redef]
        for i, movement in enumerate(keypad_movement_permutations(a, b)):
            p0 = "A"
            for p1 in movement:
                subtotal, p0 = shortest_length(p0, p1, max_depth, depth+1)
                counts[i] += subtotal
        total += min(counts.values())

    else:
        counts: dict[int, int] = defaultdict(int)  # type: ignore[no-redef]
        for i, movement in enumerate(keypad_movement_permutations(a, b)):
            counts[i] = len(movement)
        total += min(counts.values())

    return total, b


def solve(input: str, max_depth: int) -> int:
    """
    Reusable for parts 1 and 2 with just a change to the max recursion depth.
    """
    result = 0

    for code in input.strip().split("\n"):
        numeric = int("".join(c for c in code if c.isdigit()))

        total = 0
        last = "A"
        for c in code:
            subtotal, last = shortest_length(last, c, max_depth)
            total += subtotal

        complexity = numeric * total
        result += complexity

    return result


def part1(input: str) -> int:
    return solve(input, 2)


def part2(input: str) -> int:
    return solve(input, 25)


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day21_example.txt", part1, 126384),
        ("Part 1", "inputs/day21_full.txt", part1, 163920),
        ("Part 2", "inputs/day21_full.txt", part2, 204040805018350),
    ):
        path = Path(__file__).parent / filename
        with open(path) as f:
            contents = f.read()

        # Different inputs and puzzle parts should not interfere (in order to
        # get more accurate per-part timing)
        numpad_movement_permutations.cache_clear()
        keypad_movement_permutations.cache_clear()
        shortest_length.cache_clear()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
