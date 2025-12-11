from functools import cache
from io import StringIO
from pathlib import Path
from time import time

YEAR = 2025
DAY = 11
NAME = "Reactor"

PRINT_GRAPHVIZ = False


def parse_input(input: str) -> dict[str, list[str]]:
    adjacencies: dict[str, list[str]] = dict()

    for line in input.strip().split("\n"):
        parts = line.split()
        device = parts[0].strip(":")
        outputs = parts[1:]

        if device not in adjacencies:
            adjacencies[device] = list()

        for output in outputs:
            adjacencies[device].append(output)
            if output not in adjacencies:
                adjacencies[output] = list()

    return adjacencies


def to_graphviz(
        adjacencies: dict[str, list[str]], colours: dict[str, str]) -> str:
    """
    Yep, visualising the input structure is super useful for Advent of Code.
    """
    buf = StringIO()

    buf.write("digraph G {\n")

    if colours:
        buf.write("\n")
        for name, fillcolor in colours.items():
            buf.write(f"\t{name} [style=filled fillcolor={fillcolor} fontcolor=white]\n")  # noqa: E501
        buf.write("\n")

    for k, V in adjacencies.items():
        for v in V:
            buf.write(f"\t{k} -> {v}\n")

    buf.write("}")

    return buf.getvalue()


def calc_num_paths(
        adjacencies: dict[str, list[str]],
        src: str,
        dst: str,
        required: frozenset[str]
) -> int:
    @cache
    def visit(current: str, seen: frozenset[str]) -> int:
        if current == dst:
            return 1 if seen == required else 0
        else:
            n = 0
            for a in adjacencies[current]:
                # Copy this so seeing a node for one adjacency doesn't affect
                # the others
                copied_seen = set(seen)
                if a in required:
                    copied_seen.add(a)
                n += visit(a, frozenset(copied_seen))
            return n

    num = visit(src, frozenset())
    return num


def part1(input: str) -> int:
    adjacencies = parse_input(input)

    src = "you"
    dst = "out"
    required: frozenset[str] = frozenset()

    if PRINT_GRAPHVIZ:
        print(to_graphviz(adjacencies, {
            src: "darkolivegreen3",
            dst: "orangered"
        }))

    num_paths = calc_num_paths(adjacencies, src, dst, required)
    return num_paths


def part2(input: str) -> int:
    adjacencies = parse_input(input)

    src = "svr"
    dst = "out"
    required: frozenset[str] = frozenset(["dac", "fft"])

    if PRINT_GRAPHVIZ:
        colors = {
            src: "darkolivegreen3",
            dst: "orangered",
        }
        for name in required:
            colors[name] = "orange"
        print(to_graphviz(adjacencies, colors))

    num_paths = calc_num_paths(adjacencies, src, dst, required)
    return num_paths


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day11_example.txt", part1, 5),
        ("Part 1", "inputs/day11_full.txt", part1, 699),
        ("Part 2", "inputs/day11_example2.txt", part2, 2),
        ("Part 2", "inputs/day11_full.txt", part2, 388893655378800),
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
