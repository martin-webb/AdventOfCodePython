from collections import deque
from pathlib import Path
from time import time

YEAR = 2016
DAY = 20
NAME = "Firewall Rules"

MAX = 4294967295


def parse_input(input: str) -> list[tuple[int, int]]:
    blocked: list[tuple[int, int]] = list()

    for line in input.strip().split("\n"):
        parts = line.split("-")
        block = (int(parts[0]), int(parts[1]))
        blocked.append(block)

    return blocked


def find_allowed_ranges(
        blocked: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Interval splitting.
    """
    allowed = [(0, MAX)]

    # Queue so we can revisit a block range after splitting the allowed ranges.
    Q = deque(blocked)
    while Q:
        block_min, block_max = Q.popleft()

        for i in range(len(allowed)-1, -1, -1):
            allow = allowed[i]

            # Iterate backwards over the allow ranges so we can remove blocked
            # range parts on the way, deleting first, then add any new allow
            # ranges at the end
            added = []

            if block_min >= allow[0] and block_max <= allow[1]:
                # Block contained entirely within the allow (2-split)
                del allowed[i]
                added.append((allow[0], block_min-1))
                added.append((block_max+1, allow[1]))
                Q.append((block_min, block_max))

            elif block_min <= allow[0] and block_max >= allow[1]:
                # Block fully outside the allow (no split, just remove)
                del allowed[i]

            elif allow[0] <= block_min <= allow[1]:
                # Block minimum contained in the allow (1-split)
                del allowed[i]
                added.append((allow[0], block_min-1))
                Q.append((block_min, block_max))

            elif allow[0] <= block_max <= allow[1]:
                # Block maximum contained in the allow (1-split)
                del allowed[i]
                added.append((block_max+1, allow[1]))
                Q.append((block_min, block_max))

            allowed += added

    return allowed


def part1(input: str) -> int:
    blocked = parse_input(input)
    allowed = find_allowed_ranges(blocked)
    result = sorted(allowed)[0][0]
    return result


def part2(input: str) -> int:
    blocked = parse_input(input)
    allowed = find_allowed_ranges(blocked)
    result = sum([allow[1] - allow[0] + 1 for allow in allowed])
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day20_full.txt", part1, 19449262),
        ("Part 2", "inputs/day20_full.txt", part2, 119)
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
