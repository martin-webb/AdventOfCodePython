from time import time

YEAR = 2023
DAY = 9
NAME = "Mirage Maintenance"

PRINT_VISUALISATION = False


def part1(input: str) -> int:
    def extrapolate(numbers: list[int], depth: int = 0) -> int:
        indent = " " * depth
        if PRINT_VISUALISATION:
            print(f"{indent}{' '.join([str(n) for n in numbers])}")
        # Is this a fair assumption? numbers[0] and numbers[1] independently
        # don't indicate a full set of zero-differences, and neither does
        # sum(numbers) == 0 (both of these can be shown to have cases where
        # this check is invalid).
        # Is there a case where numbers[0] and numbers[-1] can both be zero but
        # the intermediate numbers won't be? I don't believe so, as with these
        # rules the differences will always be increasing or decreasing, but
        # this could be a faulty assumption. Anyway, let's just do an explicit
        # check for all differences.
        if all(n == 0 for n in numbers):
            if PRINT_VISUALISATION:
                print(f"{indent}{' '.join([str(n) for n in numbers])} [0]")
            return 0
        else:
            diffs = [
                b - a for a, b in zip(numbers[:len(numbers) - 1], numbers[1:])
            ]
            extrapolated = extrapolate(diffs, depth + 1)
            if PRINT_VISUALISATION:
                print(f"{indent}{' '.join([str(n) for n in numbers])} " +
                      f"[{numbers[-1] + extrapolated}]")
            return numbers[-1] + extrapolated

    total = 0

    lines = input.strip().split("\n")
    for line in lines:
        nums = [int(n) for n in line.split()]
        extrapolated = extrapolate(nums)
        total += extrapolated

    return total


def part2(input: str) -> int:
    def extrapolate(numbers: list[int], depth: int = 0) -> int:
        indent = " " * depth
        if PRINT_VISUALISATION:
            print(f"{indent}{' '.join([str(n) for n in numbers])}")
        # Is this a fair assumption? numbers[0] and numbers[1] independently
        # don't indicate a full set of zero-differences, and neither does
        # sum(numbers) == 0 (both of these can be shown to have cases where
        # this check is invalid).
        # Is there a case where numbers[0] and numbers[-1] can both be zero but
        # the intermediate numbers won't be? I don't believe so, as with these
        # rules the differences will always be increasing or decreasing, but
        # this could be a faulty assumption. Anyway, let's just do an explicit
        # check for all differences.
        if all(n == 0 for n in numbers):
            if PRINT_VISUALISATION:
                print(f"{indent}[0] {' '.join([str(n) for n in numbers])}")
            return 0
        else:
            diffs = [
                b - a for a, b in zip(numbers[:len(numbers) - 1], numbers[1:])
            ]
            extrapolated = extrapolate(diffs, depth + 1)
            if PRINT_VISUALISATION:
                print(f"{indent}[{numbers[0] - extrapolated}] "
                      f"{' '.join([str(n) for n in numbers])}")
            return numbers[0] - extrapolated

    total = 0

    lines = input.strip().split("\n")
    for line in lines:
        nums = [int(n) for n in line.split()]
        extrapolated = extrapolate(nums)
        total += extrapolated

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day09_example.txt", part1, 114),
        ("Part 1", "inputs/day09_full.txt", part1, 1953784198),
        ("Part 2", "inputs/day09_example.txt", part2, 2),
        ("Part 2", "inputs/day09_full.txt", part2, 957),
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
