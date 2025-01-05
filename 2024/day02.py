from time import time

DAY = 2
NAME = "Red-Nosed Reports"


def is_safe(values: list[int], direction: int, i: int = 1) -> bool:
    assert direction == 1 or direction == -1

    diff = values[i] - values[i-1]
    if direction == 1:
        safe = diff > 0 and abs(diff) >= 1 and abs(diff) <= 3
    elif direction == -1:
        safe = diff < 0 and abs(diff) >= 1 and abs(diff) <= 3

    is_last = i == len(values) - 1
    if is_last:
        return safe
    else:
        return is_safe(values, direction, i+1) if safe else False


def part1(input: str) -> int:
    total = 0

    for line in input.strip().split("\n"):
        N = [int(n) for n in line.split()]
        direction = 1 if N[1] - N[0] > 0 else -1
        safe = is_safe(N, direction)
        if safe:
            total += 1

    return total


def part2(input: str) -> int:
    total = 0

    for line in input.strip().split("\n"):
        N = [int(n) for n in line.split()]
        at_least_one_safe = False

        # Generate report variations
        for i in range(len(N)):
            NN = N[:i] + N[i+1:]
            direction = 1 if NN[1] - NN[0] > 0 else -1
            safe = is_safe(NN, direction)
            if safe:
                at_least_one_safe = True
                break
        if at_least_one_safe:
            total += 1

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day02_example.txt", part1, 2),
        ("Part 1", "inputs/day02_full.txt", part1, 236),
        ("Part 2", "inputs/day02_example.txt", part2, 4),
        ("Part 2", "inputs/day02_full.txt", part2, 308),
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
