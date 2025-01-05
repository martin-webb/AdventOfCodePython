from time import time

YEAR = 2023
DAY = 2
NAME = "Cube Conundrum"


def part1(input: str) -> int:
    possible_game_id_sum = 0

    for line in input.strip().split("\n"):
        line_norm = line.strip()
        label, description = line_norm.split(":")
        game_id = label.split()[1]
        bag_draws = description.split(";")
        counts = {"red": 0, "blue": 0, "green": 0}
        for draw in bag_draws:
            cols = draw.split(",")
            for col in cols:
                num_str, colour = col.split()
                num = int(num_str.strip())
                colour = colour.strip()
                if num > counts[colour]:
                    counts[colour] = num

        if (
            counts["red"] <= 12
            and counts["green"] <= 13
            and counts["blue"] <= 14
        ):
            possible_game_id_sum += int(game_id)

    return possible_game_id_sum


def part2(input: str) -> int:
    sum_of_powers = 0

    for line in input.strip().split("\n"):
        line = line.strip()
        description = line.split(":")[1]
        bag_draws = description.split(";")
        counts = {"red": 0, "blue": 0, "green": 0}
        for draw in bag_draws:
            cols = draw.split(",")
            for col in cols:
                num_str, colour = col.split()
                num = int(num_str.strip())
                colour = colour.strip()
                if num > counts[colour]:
                    counts[colour] = num

        power = counts["red"] * counts["green"] * counts["blue"]
        sum_of_powers += power

    return sum_of_powers


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day02_example.txt", part1, 8),
        ("Part 1", "inputs/day02_full.txt", part1, 2795),
        ("Part 2", "inputs/day02_example.txt", part2, 2286),
        ("Part 2", "inputs/day02_full.txt", part2, 75561),
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
