from time import time

YEAR = 2024
DAY = 4
NAME = "Ceres Search"


def find_word(
        needle: str,
        rows: list[list[str]],
        x: int,
        y: int,
        dx: int,
        dy: int) -> int:
    for i in range(len(needle)):
        xx = x + i * dx
        yy = y + i * dy
        if xx < 0 or xx >= len(rows[0]) or yy < 0 or yy >= len(rows):
            break
        if rows[yy][xx] != needle[i]:
            break
        if i == len(needle) - 1:
            return True
    return False


def part1(input: str) -> int:
    total = 0

    rows = []
    for line in input.strip().split("\n"):
        rows.append(list(line))

    for y in range(len(rows)):
        for x in range(len(rows[0])):
            # Technically we'll compare the X again in find_word(), however
            # this makes it easy to reuse for both parts
            if rows[y][x] == "X":
                if find_word("XMAS", rows, x, y, -1, -1):
                    total += 1
                if find_word("XMAS", rows, x, y,  0, -1):
                    total += 1
                if find_word("XMAS", rows, x, y,  1, -1):
                    total += 1
                if find_word("XMAS", rows, x, y, -1,  0):
                    total += 1
                if find_word("XMAS", rows, x, y,  1,  0):
                    total += 1
                if find_word("XMAS", rows, x, y, -1,  1):
                    total += 1
                if find_word("XMAS", rows, x, y,  0,  1):
                    total += 1
                if find_word("XMAS", rows, x, y,  1,  1):
                    total += 1

    return total


def part2(input: str) -> int:
    total = 0

    rows = []
    for line in input.strip().split("\n"):
        rows.append(list(line))

    for y in range(len(rows)):
        for x in range(len(rows[0])):
            if rows[y][x] == "A":
                is_down_right = find_word("MAS", rows, x-1, y-1, 1, 1)
                is_down_left = find_word("MAS", rows, x+1, y-1, -1, 1)
                is_up_right = find_word("MAS", rows, x-1, y+1, 1, -1)
                is_up_left = find_word("MAS", rows, x+1, y+1, -1, -1)
                if (
                    (is_down_right or is_up_left) and
                    (is_down_left or is_up_right)
                ):
                    total += 1

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day04_example.txt", part1, 18),
        ("Part 1", "inputs/day04_full.txt", part1, 2447),
        ("Part 2", "inputs/day04_example.txt", part2, 9),
        ("Part 2", "inputs/day04_full.txt", part2, 1868),
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
