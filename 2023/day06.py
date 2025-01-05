from time import time

YEAR = 2023
DAY = 6
NAME = "Wait For It"


def part1(input: str) -> int:
    for line in input.strip().split("\n"):
        if line.startswith("Time"):
            times = [int(n) for n in line.split("Time:")[1].split()]
        if line.startswith("Distance"):
            distances = [int(n) for n in line.split("Distance:")[1].split()]

    races = zip(times, distances)
    races_to_num_ways_to_win = {}
    for race in races:
        winning_hold_times = []
        time = race[0]
        distance = race[1]
        for i in range(0, time + 1):
            speed = i
            remaining_time = time - i
            actual_distance = speed * remaining_time
            if actual_distance > distance:
                winning_hold_times.append(i)
        races_to_num_ways_to_win[race] = len(winning_hold_times)

    total = 1
    for race, num in races_to_num_ways_to_win.items():
        total *= num

    return total


def part2(input: str) -> int:
    for line in input.strip().split("\n"):
        if line.startswith("Time"):
            time = int(line.split("Time:")[1].replace(" ", ""))
        if line.startswith("Distance"):
            distance = int(line.split("Distance:")[1].replace(" ", ""))

    threshold_min = None
    for i in range(0, time + 1):
        speed = i
        remaining_time = time - i
        actual_distance = speed * remaining_time
        if actual_distance > distance:
            threshold_min = i
            break

    threshold_max = None
    for i in range(time, -1, -1):
        speed = i
        remaining_time = time - i
        actual_distance = speed * remaining_time
        if actual_distance > distance:
            threshold_max = i
            break

    assert threshold_min is not None
    assert threshold_max is not None

    winning_hold_times = threshold_max - threshold_min + 1
    return winning_hold_times


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day06_example.txt", part1, 288),
        ("Part 1", "inputs/day06_full.txt", part1, 503424),
        ("Part 2", "inputs/day06_example.txt", part2, 71503),
        ("Part 2", "inputs/day06_full.txt", part2, 32607562),
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
