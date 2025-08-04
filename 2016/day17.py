from collections import deque
from hashlib import md5
from pathlib import Path
from time import time

YEAR = 2016
DAY = 17
NAME = "Two Steps Forward"

START = (0, 0)
END = (3, 3)
DOOR_OPEN_CHARS = set("bcdef")


def visit(
        coords: tuple[int, int],
        password: str) -> list[tuple[tuple[int, int], str]]:
    neighbours = list()

    h = md5(password.encode("utf-8"))
    digest = h.hexdigest()

    neighbours_by_direction = {
        (0, -1): (digest[0] in DOOR_OPEN_CHARS, "U"),
        (0, 1): (digest[1] in DOOR_OPEN_CHARS, "D"),
        (-1, 0): (digest[2] in DOOR_OPEN_CHARS, "L"),
        (1, 0): (digest[3] in DOOR_OPEN_CHARS, "R")
    }

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for direction in directions:
        neighbour = (coords[0] + direction[0], coords[1] + direction[1])
        if not (0 <= neighbour[0] <= 3 and 0 <= neighbour[1] <= 3):
            continue

        is_open = neighbours_by_direction[direction][0]
        if not is_open:
            continue

        direction_char = neighbours_by_direction[direction][1]
        neighbours.append((neighbour, password + direction_char))

    return neighbours


def part1(input: str) -> str:
    path = None

    original_password = input.strip()

    Q = deque([(START, original_password)])
    while Q:
        coords, password = Q.popleft()

        if coords == END:
            path = password[len(original_password):]
            break

        for next_coords, next_password in visit(coords, password):
            candidate = (next_coords, next_password)
            # NOTE: Breadth-first search over the space.
            # NOTE: We could prioritise certain movement directions here, that
            # is, prefer moving (say) down or right, but this doesn't make a
            # difference.
            Q.append(candidate)

    assert path is not None, "No path found"
    return path


def part2(input: str) -> int:
    longest_path = 0

    original_password = input.strip()

    Q = deque([(START, original_password)])
    while Q:
        coords, password = Q.popleft()

        if coords == END:
            path = password[len(original_password):]
            longest_path = max(longest_path, len(path))
            continue

        for next_coords, next_password in visit(coords, password):
            candidate = (next_coords, next_password)
            # As we're searching the full space without pruning there's no
            # advantage to either breadth-first of depth-first search here.
            Q.append(candidate)

    return longest_path


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day17_full.txt", part1, "DUDRLRRDDR"),
        ("Part 2", "inputs/day17_full.txt", part2, 788),
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
