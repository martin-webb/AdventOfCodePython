import re
from time import time

YEAR = 2023
DAY = 1
NAME = "Trebuchet?!"

PATTERN = re.compile(r"""(?=(one|two|three|four|five|six|seven|eight|nine))""")

WORDS_TO_NUMS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def part1(input: str) -> int:
    total = 0

    for line in input.strip().split("\n"):
        calibration = 0

        for char in line[::1]:
            if char.isdigit():
                calibration += int(char) * 10
                break
        else:
            raise RuntimeError("No left digit found")

        for char in line[::-1]:
            if char.isdigit():
                calibration += int(char)
                break
        else:
            raise RuntimeError("No right digit found")

        total += calibration

    return total


def part2(input: str) -> int:
    total = 0

    for line in input.strip().split("\n"):
        left = ""
        right = ""

        left_digit = ""
        left_digit_pos = None
        for i, char in enumerate(line[::1]):
            if char.isdigit():
                left_digit = char
                left_digit_pos = i
                break

        right_digit = ""
        right_digit_pos = None
        for i, char in enumerate(line[::-1]):
            if char.isdigit():
                right_digit = char
                right_digit_pos = len(line) - i - 1
                break

        matches = list(re.finditer(PATTERN, line))
        if len(matches) > 0:
            match = matches[0]
            if left_digit_pos is not None and left_digit_pos < match.start():
                left = left_digit
            else:
                left = str(WORDS_TO_NUMS[match.group(1)])

            match = matches[-1]
            if right_digit_pos is not None and right_digit_pos > match.start():
                right = right_digit
            else:
                right = str(WORDS_TO_NUMS[match.group(1)])
        else:
            left = left_digit
            right = right_digit

        calibration = int(left + right)
        total += calibration

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day01_part1_example.txt", part1, 142),
        ("Part 1", "inputs/day01_full.txt", part1, 53080),
        ("Part 2", "inputs/day01_part2_example.txt", part2, 281),
        ("Part 2", "inputs/day01_full.txt", part2, 53268),
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
