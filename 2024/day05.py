from collections import defaultdict, deque
from math import floor
from pathlib import Path
from time import time

YEAR = 2024
DAY = 5
NAME = "Print Queue"


def make_rules(lines: list[str], pages: list[int]) -> dict[int, list[int]]:
    """
    Make map of report-specific page dependencies based on the subset of all
    the dependencies that are relevant for the given page numbers.
    This allows us to create a directed acyclic graph that can be sorted
    topologically (using all of the available rules can result in a cycle).
    """
    rules: dict[int, list[int]] = defaultdict(list)

    for line in lines:
        a, b = [int(x) for x in line.split("|")]
        # Only create dependencies for the given pages
        if a in pages and b in pages:
            rules[b].append(a)

    return rules


def sort_pages(pages: list[int], rules: dict[int, list[int]]) -> list[int]:
    """
    Topological sort of pages using DFS and rules dependency list.
    """
    def visit(
            n: int,
            rules: dict[int, list[int]],
            temp: set[int],
            result: list[int]) -> None:
        if n in result:
            return
        if n in temp:
            raise RuntimeError("Cycle detected")

        temp.add(n)
        for dependency in rules.get(n, []):
            visit(dependency, rules, temp, result)
        result.append(n)

    result: list[int] = []

    unvisited = deque(pages)
    while unvisited:
        n = unvisited.popleft()
        temp: set[int] = set()
        visit(n, rules, temp, result)

    return result


def part1(input: str) -> int:
    """
    NOTE: Part 1 can be done without a topological sort and just a simple check
    of dependencies (and can be faster this way), but as this approach is used
    for part 2 to get sorted pages then we can also use that here to determine
    which of the reports are already in the right order, making both parts
    almost the same.
    """
    total = 0

    rules_input, updates_input = input.strip().split("\n\n")

    for update in updates_input.split("\n"):
        pages = [int(x) for x in update.split(",")]
        rules = make_rules(rules_input.split("\n"), pages)

        sorted_pages = sort_pages(pages, rules)

        if pages == sorted_pages:
            # Assuming odd number of pages so there's always a middle
            middle_index = int(floor(len(pages) / 2.0))
            total += pages[middle_index]

    return total


def part2(input: str) -> int:
    total = 0

    rules_input, updates_input = input.strip().split("\n\n")

    for update in updates_input.split("\n"):
        pages = [int(x) for x in update.split(",")]
        rules = make_rules(rules_input.split("\n"), pages)

        sorted_pages = sort_pages(pages, rules)

        if pages != sorted_pages:
            # Assuming odd number of pages so there's always a middle
            middle_index = int(floor(len(pages) / 2.0))
            total += sorted_pages[middle_index]

    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day05_example.txt", part1, 143),
        ("Part 1", "inputs/day05_full.txt", part1, 4462),
        ("Part 2", "inputs/day05_example.txt", part2, 123),
        ("Part 2", "inputs/day05_full.txt", part2, 6767),
    ):
        path = Path(__file__).parent / filename
        with open(path) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
