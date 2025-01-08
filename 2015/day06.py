from pathlib import Path
from time import time

YEAR = 2015
DAY = 6
NAME = "Probably a Fire Hazard"


def parse_line(line: str) -> tuple[str, int, int, int, int]:
    """
    Parse input line into 5-tuple of the form:
        (command, src_x, src_y, dst_x, dst_y)
    """
    parts = line.split()
    if len(parts) == 4:  # "toggle"
        command = parts[0]
        src_s, dst_s = parts[1], parts[3]
    elif len(parts) == 5:  # "turn on" / "turn off"
        command = parts[1]
        src_s, dst_s = parts[2], parts[4]

    src_x, src_y = [int(x) for x in src_s.split(",")]
    dst_x, dst_y = [int(x) for x in dst_s.split(",")]

    return command, src_x, src_y, dst_x, dst_y


def part1(input: str) -> int:
    lights = []
    for _ in range(1000):
        lights.append([0] * 1000)

    for line in input.strip().split("\n"):
        command, src_x, src_y, dst_x, dst_y = parse_line(line)

        if command == "on":
            for y in range(src_y, dst_y + 1):
                for x in range(src_x, dst_x + 1):
                    lights[y][x] = 1

        elif command == "off":
            for y in range(src_y, dst_y + 1):
                for x in range(src_x, dst_x + 1):
                    lights[y][x] = 0

        elif command == "toggle":
            for y in range(src_y, dst_y + 1):
                for x in range(src_x, dst_x + 1):
                    lights[y][x] = 1 - lights[y][x]

    return sum([sum(row) for row in lights])


def part2(input: str) -> int:
    lights = []
    for _ in range(1000):
        lights.append([0] * 1000)

    for line in input.strip().split("\n"):
        command, src_x, src_y, dst_x, dst_y = parse_line(line)

        if command == "on":
            for y in range(src_y, dst_y + 1):
                for x in range(src_x, dst_x + 1):
                    lights[y][x] += 1

        elif command == "off":
            for y in range(src_y, dst_y + 1):
                for x in range(src_x, dst_x + 1):
                    lights[y][x] = max(lights[y][x] - 1, 0)

        elif command == "toggle":
            for x in range(src_x, dst_x + 1):
                for y in range(src_y, dst_y + 1):
                    lights[y][x] += 2

    return sum([sum(row) for row in lights])


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day06_full.txt", part1, 569999),
        ("Part 2", "inputs/day06_full.txt", part2, 17836115)
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
