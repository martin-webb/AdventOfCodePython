from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappop, heappush
from pathlib import Path
from typing import Optional
from time import time

YEAR = 2023
DAY = 17
NAME = "Clumsy Crucible"


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x},{self.y})"


@dataclass(eq=True, order=True, frozen=True)
class Vertex:
    position: tuple[int, int]
    src: Optional[tuple[int, int]]
    direction: tuple[int, int]
    weight: int = field(compare=False)


@dataclass(order=True)
class PriorityEntry:
    distance: int
    vertex: Vertex = field(compare=False)
    previous: Optional[Vertex] = field(compare=False)


def sum_distance(start: Vertex,
                 dest: Vertex,
                 previous_vertices: dict[Vertex, Optional[Vertex]]) -> int:
    total = 0
    current = start
    while current != dest:
        total += current.weight
        current = previous_vertices[current]  # type: ignore[assignment]

    return total


def find_minimum_heat_loss(vertices: list[Vertex], start: Vertex) -> int:
    """
    Min-heap implementation of Dijkstra's Algorithm that also accounts for our
    graph having multiple 'variants' of the same node that differ by the
    constrained paths that can be taken to arrive there and uses a custom heap
    entry which keeps both the vertex and previous vertex associated with the
    distance/priority.
    """
    # Used only to stop us from needing to iterate over all nodes for each node
    # when building adjacency lists
    src_to_vertices = defaultdict(list)
    for v in vertices:
        src_to_vertices[v.src].append(v)

    # Adjacency lists
    neighbours = defaultdict(list)
    for v in vertices:
        excluded_directions = (
            v.direction,
            (v.direction[0] * -1, v.direction[1] * -1)  # Backwards
        )

        # This applies the constraint about having to turn on entering a node
        # and not being able to backtrack. We don't need to check any distance
        # moved here as our graph represents distances moved as separate
        # vertices, so each vertex adjacency list already encodes the
        # maximum-distance-before-turn constraint
        # If our vertices DID represent all possible movement distances then
        # we could apply that constraint here, however that would add a lot of
        # additional vertices that would never be included in any adjacencies,
        # so let's just not do that
        neighbours[v] = [n for n in src_to_vertices[v.position]
                         if n.direction not in excluded_directions]

    src_to_vertices = defaultdict(list)
    positions_to_vertices = defaultdict(list)
    for v in vertices:
        src_to_vertices[v.src].append(v)
        positions_to_vertices[v.position].append(v)

    neighbours = defaultdict(list)
    for v in vertices:
        excluded_directions = (
            v.direction,
            (v.direction[0] * -1, v.direction[1] * -1)  # Backwards
        )

        # This applies the constraint about having to turn on entering a node
        # and not being able to backtrack. We don't need to check any distance
        # moved here as our graph represents distances moved as separate
        # vertices, so each vertex adjacency list already encodes the
        # maximum-distance-before-turn constraint
        # If our vertices DID represent all possible movement distances then
        # we could apply that constraint here, however that would add a lot of
        # additional vertices that would never be included in any adjacencies,
        # so let's just not do that
        neighbours[v] = [n for n in src_to_vertices[v.position]
                         if n.direction not in excluded_directions]

    heap = [PriorityEntry(distance=0, vertex=start, previous=None)]
    shortest_distances = {}
    previous_vertices = {}

    while heap:
        item = heappop(heap)
        if item.vertex in shortest_distances:
            continue

        shortest_distances[item.vertex] = item.distance
        previous_vertices[item.vertex] = item.previous

        for n in neighbours[item.vertex]:
            if n not in shortest_distances:
                heappush(
                    heap,
                    PriorityEntry(item.distance + n.weight, n, item.vertex)
                )

    # As there are multiple ways we can end up at the destination as our graph
    # structure allows 'variants' of each vertex, we need to check all for the
    # shortest distance amongst all shortest distances...
    end_pos = max(v.position for v in vertices)
    end_nodes = [node for node in shortest_distances
                 if node.position == end_pos]

    heat_losses = [sum_distance(end_node, start, previous_vertices)
                   for end_node in end_nodes]

    minimum_heat_loss = min(heat_losses)
    return minimum_heat_loss


def part1(input: str) -> int:
    lines = input.strip().split("\n")

    grid = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x, y)] = int(char)

    x_max = x
    y_max = y

    vertices = []

    start = Vertex(
        position=(0, 0),
        src=(0, 0),
        direction=(0, 0),
        weight=0
    )
    vertices.append(start)

    for y in range(y_max + 1):
        for x in range(x_max + 1):
            src = (x, y)
            for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # Combined weight as movements of 1, 2 and 3 squares are
                # represented as unique vertices, and for a multi-step movement
                # we still need the weight of all movements made to get to that
                # vertex
                combined_weight = 0
                # This encodes the constraint that movement can be up to three
                # squares in a line before having to turn
                # The other requirements for changing not traveling backwards
                # and having to turn left or right are handled whe setting up
                # the adjacency lists
                for i in range(1, 4):
                    dst = (
                        src[0] + (direction[0] * i),
                        src[1] + (direction[1] * i)
                    )
                    if dst not in grid:
                        break
                    combined_weight += grid[dst]
                    vertex = Vertex(
                        position=dst,
                        src=src,
                        direction=direction,
                        weight=combined_weight
                    )
                    vertices.append(vertex)

    minimum_heat_loss = find_minimum_heat_loss(vertices, start)
    return minimum_heat_loss


def part2(input: str) -> int:
    lines = input.strip().split("\n")

    grid = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x, y)] = int(char)

    x_max = x
    y_max = y

    vertices = []

    start = Vertex(
        position=(0, 0),
        src=(0, 0),
        direction=(0, 0),
        weight=0
    )
    vertices.append(start)

    for y in range(y_max + 1):
        for x in range(x_max + 1):
            src = (x, y)
            for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # Combined weight as movements of 1, 2 and 3 squares are
                # represented as unique vertices, and for a multi-step movement
                # we still need the weight of all movements made to get to that
                # vertex
                combined_weight = 0
                # > Once an ultra crucible starts moving in a direction, it
                # > needs to move a minimum of four blocks in that direction
                # > before it can turn (or even before it can stop at the end).
                # > However, it will eventually start to get wobbly: an ultra
                # > crucible can move a maximum of ten consecutive blocks
                # > without turning.
                # This encodes this constraint.
                # NOTE: we still need to sum weights from distances 1, 2 and 3
                # but we don't include them as possible vertices
                for i in range(1, 11):
                    dst = (
                        src[0] + (direction[0] * i),
                        src[1] + (direction[1] * i)
                    )
                    if dst not in grid:
                        break
                    combined_weight += grid[dst]
                    if i >= 4:
                        vertex = Vertex(
                            position=dst,
                            src=src,
                            direction=direction,
                            weight=combined_weight
                        )
                        vertices.append(vertex)

    minimum_heat_loss = find_minimum_heat_loss(vertices, start)
    return minimum_heat_loss


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day17_example.txt", part1, 102),
        ("Part 1", "inputs/day17_full.txt", part1, 843),
        ("Part 2", "inputs/day17_example.txt", part2, 94),
        ("Part 2", "inputs/day17_example_part2_extra.txt", part2, 71),
        ("Part 2", "inputs/day17_full.txt", part2, 1017),
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
