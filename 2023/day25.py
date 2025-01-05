from copy import deepcopy
from collections import defaultdict, deque
from dataclasses import dataclass
import random
from time import time

YEAR = 2023
DAY = 25
NAME = "Snowverload"


@dataclass
class Edge:
    v1: str
    v1_original: str
    v2: str
    v2_original: str


def traverse(vertex: str, adjacencies: dict[str, set[str]]) -> set[str]:
    """
    Find vertices reachable from the given vertex with the adjacency sets.
    """
    visited = set()

    to_visit = deque([vertex])
    while to_visit:
        v1 = to_visit.popleft()
        visited.add(v1)
        for v2 in adjacencies[v1]:
            if v2 not in visited:  # Don't follow cycles
                to_visit.append(v2)

    return visited


def collapse(vertices: set[str],
             adjacencies: dict[str, set[str]],
             edges: list[Edge]) -> \
                tuple[set[str], dict[str, set[str]], list[Edge]]:
    """
    Collapse graph using Karger's algorithm.
    """
    vertices = deepcopy(vertices)
    adjacencies = deepcopy(adjacencies)
    edges = deepcopy(edges)

    while len(vertices) > 2:
        edge = random.choice(edges)
        s, t = edge.v1, edge.v2

        # Update adjacencies
        for tn in set(adjacencies[t]):
            if tn != s:
                adjacencies[tn].remove(t)
                adjacencies[tn].add(s)
                adjacencies[s].add(tn)

        adjacencies[s].remove(t)
        del adjacencies[t]

        st_edge_indices = [i for i, e in enumerate(edges)
                           if (e.v1 == s and e.v2 == t)
                           or (e.v1 == t and e.v2 == s)]
        for i in sorted(st_edge_indices, reverse=True):
            del edges[i]

        # Update edge list (edges referencing T now reference S)
        for e in edges:
            if e.v1 == t:
                e.v1 = s
            elif e.v2 == t:
                e.v2 = s

        # Remove self loops (we can't collapse a vertex on itself)
        loop_edge_indices = [i for i, e in enumerate(edges) if e.v1 == e.v2]
        for i in sorted(loop_edge_indices, reverse=True):
            del edges[i]

        vertices.remove(t)

    return vertices, adjacencies, edges


def part1(input: str) -> int:
    vertices: set[str] = set()
    adjacencies: dict[str, set[str]] = defaultdict(set)

    for line in input.strip().split("\n"):
        v1, *v2s = line.replace(":", "").split()
        vertices.add(v1)
        for v2 in v2s:
            vertices.add(v2)
            adjacencies[v1].add(v2)
            adjacencies[v2].add(v1)

    edge_set = set()
    for v1, v2s in adjacencies.items():  # type: ignore[assignment]
        for v2 in v2s:
            edge_set.add((v1, v2))
            edge_set.add((v2, v1))

    edges: list[Edge] = []
    for e in edge_set:
        edge = Edge(v1=e[0], v1_original=e[0], v2=e[1], v2_original=e[1])
        edges.append(edge)

    while True:
        _, _, updated_edges = collapse(vertices, adjacencies, edges)
        # NOTE: 6 not 3 as we represent bidirectional edges with two entries
        if len(updated_edges) == 6:
            break

    # Update adjacencies and edges based on collapsed. This means removing the
    # remaining edges and adjacencies from the original graph to give us a
    # structure we can
    for e in updated_edges:  # type: ignore[assignment]
        v1 = e.v1_original  # type: ignore[attr-defined]
        v2 = e.v2_original  # type: ignore[attr-defined]
        if v1 in adjacencies:
            adjacencies[v1].remove(v2)

    sub_a = traverse(updated_edges[0].v1, adjacencies)
    sub_b = traverse(updated_edges[0].v2, adjacencies)

    total = len(sub_a) * len(sub_b)
    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day25_example.txt", part1, 54),
        ("Part 1", "inputs/day25_full.txt", part1, 598120),
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
