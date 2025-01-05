from collections import defaultdict, deque
from itertools import combinations
from time import time
from typing import cast

YEAR = 2024
DAY = 23
NAME = "LAN Party"


def expand_clique(
        clique: set[str], adjacencies: dict[str, set[str]]) -> set[str]:
    clique = set(clique)

    visited: set[str] = set()
    to_visit: deque[str] = deque()

    for member in clique:
        visited.add(member)
        to_visit.extend(adjacencies[member])

    while to_visit:
        candidate = to_visit.popleft()
        if candidate in visited:
            continue

        visited.add(candidate)

        connected_to_all = True
        for member in clique:
            if candidate not in adjacencies[member]:
                connected_to_all = False
                break

        if connected_to_all:
            clique.add(candidate)
            to_visit.extend(adjacencies[candidate])

    return clique


def part1(input: str) -> int:
    adjacencies: dict[str, set[str]] = defaultdict(set)

    for line in input.strip().split("\n"):
        a, b = line.split("-")
        adjacencies[a].add(b)
        adjacencies[b].add(a)

    groups: set[tuple[str, str, str]] = set()

    for a, b, c in combinations(adjacencies.keys(), 3):
        is_a_connected = b in adjacencies[a] and c in adjacencies[a]
        is_b_connected = a in adjacencies[b] and c in adjacencies[b]
        is_c_connected = a in adjacencies[c] and b in adjacencies[c]

        if is_a_connected and is_b_connected and is_c_connected:
            group = tuple(sorted(tuple([a, b, c])))
            found_historian = any([x.startswith("t") for x in group])
            if found_historian:
                groups.add(cast(tuple[str, str, str], group))

    return len(groups)


def part2(input: str) -> str:
    adjacencies: dict[str, set[str]] = defaultdict(set)

    for line in input.strip().split("\n"):
        a, b = line.split("-")
        adjacencies[a].add(b)
        adjacencies[b].add(a)

    cliques: list[set] = list()
    for a, friends in sorted(adjacencies.items()):
        for f in friends:
            clique = set([a, f])
            expanded = expand_clique(clique, adjacencies)
            cliques.append(expanded)

    sorted_cliques = sorted(cliques, key=lambda clique: len(clique))
    password = ",".join(sorted(sorted_cliques[-1]))
    return password


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day23_example.txt", part1, 7),
        ("Part 1", "inputs/day23_full.txt", part1, 1218),
        ("Part 2", "inputs/day23_example.txt", part2, "co,de,ka,ta"),
        ("Part 2", "inputs/day23_full.txt", part2,
         "ah,ap,ek,fj,fr,jt,ka,ln,me,mp,qa,ql,zg"),
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
