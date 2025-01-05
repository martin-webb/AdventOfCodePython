from itertools import cycle
from math import lcm
from time import time

DAY = 8
NAME = "Haunted Wasteland"


def part1(input: str) -> int:
    lines = input.strip().split("\n")

    directions = lines[0]
    nodes = {}
    for line in lines[2:]:
        l, r = line.split("=")
        label = l.strip()
        lresult = r.split(",")[0].strip().strip("(")
        rresult = r.split(",")[1].strip().strip(")")
        nodes[label] = (lresult, rresult)

    steps = 0
    current = "AAA"
    direction_cycler = cycle(directions)
    while current != "ZZZ":
        next_direction = next(direction_cycler)
        index = "LR".index(next_direction)
        current = nodes[current][index]
        steps += 1

    return steps


def part2(input: str) -> int:
    """
    Computationally expensive to step through all paths until on ALL end nodes
    at the same time. Instead, we start from each path independently until we
    get to an end, then find the least common multiple of all the step counts,
    as this is the number where all paths converge on an end node at the same
    time.
    NOTE: Least common multiple isn't guaranteed to work for all possible input
    cases for this problem, however it does happen to work for this specific
    puzzle input.
    """
    lines = input.strip().split("\n")

    directions = lines[0]
    nodes = {}
    for line in lines[2:]:
        l, r = line.split("=")
        label = l.strip()
        l_result = r.split(",")[0].strip().strip("(")
        r_result = r.split(",")[1].strip().strip(")")
        nodes[label] = (l_result, r_result)

    starting_nodes = [n for n in nodes.keys() if n.endswith("A")]
    starting_nodes_to_steps = {}
    for starting_node in starting_nodes:
        current = starting_node
        steps = 0
        direction_cycler = cycle(directions)
        while True:
            next_direction = next(direction_cycler)
            index = "LR".index(next_direction)
            current = nodes[current][index]
            steps += 1
            if current[-1] == "Z":
                break
        starting_nodes_to_steps[starting_node] = steps

    steps = lcm(*starting_nodes_to_steps.values())
    return steps


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day08_part1_example.txt", part1, 6),
        ("Part 1", "inputs/day08_full.txt", part1, 11911),
        ("Part 2", "inputs/day08_part1_example.txt", part2, 6),
        ("Part 2", "inputs/day08_full.txt", part2, 10151663816849),
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
