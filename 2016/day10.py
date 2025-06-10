from collections import defaultdict, deque
from collections.abc import Callable
from pathlib import Path
from time import time

YEAR = 2016
DAY = 10
NAME = "Balance Bots"


def make_bot(
        num: int,
        low_type: str,
        low_dest: int,
        high_type: str,
        high_dest: int) -> Callable:
    """
    Create a function representing a bot that will, when called with the
    current values (which bot has which microchips) and outputs state, use its
    own current values to 'pass on' the microchips to their correct locations
    (either another bot or an output), by updating the correct state dicts.
    The function also returns, in ascending order, the low and high microchip
    values that it used (not known until evaluation).
    """
    def eval(
            values: dict[int, list[int]],
            outputs: dict[int, int]) -> tuple[int, int]:
        low, high = sorted(values[num])

        if low_type == "bot":
            values[low_dest].append(low)
        else:
            outputs[low_dest] = low

        if high_type == "bot":
            values[high_dest].append(high)
        else:
            outputs[high_dest] = high
        return low, high

    return eval


def sort_bots(bots: set[int], parents: dict[int, list[int]]) -> list[int]:
    """
    Topological sort of bots using DFS and bot parent dependencies.
    """
    def visit(n: int, temp: set[int]) -> None:
        if n in result:
            return
        if n in temp:
            raise RuntimeError("Cycle detected")

        temp.add(n)
        for parent in parents.get(n, []):
            visit(parent, temp)
        result.append(n)

    result: list[int] = []

    unvisited = deque(bots)
    while unvisited:
        n = unvisited.popleft()
        temp: set[int] = set()
        visit(n, temp)

    return result


def solve(input: str) -> tuple[dict[tuple[int, int], int], dict[int, int]]:
    """
    Unnecessary closure-based solution to bot evaluation
    """
    # Simple state dicts for input, bot-microchip ownership, and output values
    values: dict[int, list[int]] = defaultdict(list)
    outputs: dict[int, int] = dict()

    # Extra dict for part 2, this stores the mapping of the low and high values
    # processed by each bot to the bot that did the processing, in order to
    # answer "what is the number of the bot that is responsible..."
    responsible_for: dict[tuple[int, int], int] = dict()

    bot_ids: set[int] = set()
    bot_parents: dict[int, list[int]] = defaultdict(list)
    bot_funcs: dict[int, Callable] = dict()

    # Parse instructions including setting up bot data and initial values
    for line in input.strip().split("\n"):
        parts = line.split()
        if parts[0] == "value":
            value = int(parts[1])
            dst = int(parts[5])

            values[dst].append(value)

        elif parts[0] == "bot":
            src = int(parts[1])
            low_type = parts[5]
            low_dest = int(parts[6])
            high_type = parts[10]
            high_dest = int(parts[11])

            bot_ids.add(src)
            bot = make_bot(src, low_type, low_dest, high_type, high_dest)

            if low_type == "bot":
                bot_ids.add(low_dest)
                bot_parents[low_dest].append(src)

            if high_type == "bot":
                bot_ids.add(high_dest)
                bot_parents[high_dest].append(src)

            bot_funcs[src] = bot

    # Evaluation loop (runs through bots in dependency-correct order)
    ordered_bot_ids = sort_bots(bot_ids, bot_parents)
    for bot_id in ordered_bot_ids:
        low, high = bot_funcs[bot_id](values, outputs)
        responsible_for[(low, high)] = bot_id

    return responsible_for, outputs


def part1(input: str) -> int:
    responsible_for, _ = solve(input)
    result = responsible_for[(17, 61)]
    return result


def part2(input: str) -> int:
    _, outputs = solve(input)
    result = outputs[0] * outputs[1] * outputs[2]
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day10_full.txt", part1, 116),
        ("Part 2", "inputs/day10_full.txt", part2, 23903),
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
