from collections import defaultdict
from dataclasses import dataclass, field
import heapq
from time import time
from typing import Optional

DAY = 16
NAME = "Reindeer Maze"


@dataclass(eq=True, frozen=True, order=True)
class Vec2i:
    x: int
    y: int


@dataclass(eq=True, frozen=True, order=True)
class Node:
    pos: Vec2i
    src: Vec2i
    direction: Vec2i
    cost: int = field(compare=False)


DIRECTIONS = [
    Vec2i(0, -1),
    Vec2i(0, 1),
    Vec2i(-1, 0),
    Vec2i(1, 0)
]


TURN_COST = 1000


def to_next_node(
    M: dict[Vec2i, str],
    pos: Vec2i,
    direction: Vec2i
) -> Optional[tuple[Vec2i, int]]:
    """
    Return next position in the given direction and the distance to it, or None
    if we hit a dead end, edge of the map or the end position.
    """
    is_vertical = direction.y != 0
    is_horizontal = direction.x != 0
    assert is_vertical or is_horizontal

    distance = 0
    while True:
        pos = Vec2i(pos.x + direction.x, pos.y + direction.y)
        distance += 1

        if M[pos] == "#":
            return None
        elif M[pos] == "E":
            break

        # Check for exits adjacent to our direction
        num_exits = 0
        if is_horizontal:
            num_exits += 1 if M[Vec2i(pos.x, pos.y - 1)] == "." else 0
            num_exits += 1 if M[Vec2i(pos.x, pos.y + 1)] == "." else 0
        elif is_vertical:
            num_exits += 1 if M[Vec2i(pos.x - 1, pos.y)] == "." else 0
            num_exits += 1 if M[Vec2i(pos.x + 1, pos.y)] == "." else 0

        if num_exits > 0:
            break

    return (pos, distance)


def build_graph(
    M: dict[Vec2i, str],
    start_pos: Vec2i,
    start_dir: Vec2i,
    end_pos: Vec2i
) -> tuple[Node, Node, set[Node], dict[Node, set[Node]]]:
    """
    Create graph from the given map, returning the start node, end node,
    node set and node adjacency map.
    """
    start = Node(start_pos, start_pos, start_dir, 0)
    end: Optional[Node] = None
    nodes: set[Node] = set()
    adjacencies: dict[Node, set[Node]] = defaultdict(set)

    visited: set = set()

    to_visit: list[tuple[int, Node]] = list()
    heapq.heappush(to_visit, (0, start))

    while to_visit:
        current_cost, node = heapq.heappop(to_visit)
        nodes.add(node)

        # We can stop as soon as we have visited the end position once
        if node.pos == end_pos:
            end = node
            break

        if node in visited:
            continue

        visited.add(node)

        for direction in DIRECTIONS:
            opposite = Vec2i(node.direction.x * -1, node.direction.y * -1)
            if direction == opposite:
                continue

            to_next_result = to_next_node(M, node.pos, direction)
            if to_next_result is None:
                continue

            (next_pos, next_distance) = to_next_result

            # If moving in the same direction add a distance node otherwise add
            # a turn node with appropriate cost, making sure to visit these in
            # an order that takes into account their node cost
            if direction == node.direction:
                cost = next_distance
                queue_cost = current_cost + cost
                next_node = Node(next_pos, node.pos, direction, cost)
            else:
                cost = TURN_COST
                queue_cost = current_cost + cost
                next_node = Node(node.pos, node.pos, direction, cost)

            nodes.add(next_node)
            adjacencies[node].add(next_node)
            heapq.heappush(to_visit, (queue_cost, next_node))

    assert end is not None

    return start, end, nodes, adjacencies


def shortest_path_and_parents(
    start: Node,
    nodes: set[Node],
    end_pos: Vec2i,
    adjacencies: dict[Node, set[Node]]
) -> tuple[int, dict[Node, set[Node]]]:
    """
    Determine the distance of the shortest path(s) in the map and a map of node
    parents, using the subset of node adjacencies determined previously.
    The map of node parents is a subset of the full set and is calculated for
    part 2, where we use this to traverse all best paths.
    """
    distances: dict[Node, float] = {n: float("inf") for n in nodes}
    distances[start] = 0

    parents: dict[Node, set[Node]] = defaultdict(set)

    to_visit: list[tuple[float, Node]] = list()
    heapq.heappush(to_visit, (0, start))

    while to_visit:
        _, u = heapq.heappop(to_visit)
        for v in adjacencies[u]:
            # NOTE: Adding a node parent link only for less-than-or-equal (and
            # NOT less-than like with the cost update below) updated distance,
            # as otherwise the search space is too large
            if v.cost + distances[u] <= distances[v]:
                parents[v].add(u)

            if v.cost + distances[u] < distances[v]:
                distances[v] = v.cost + distances[u]
                heapq.heappush(to_visit, (distances[v], v))

    end_distances = [d for (n, d) in distances.items() if n.pos == end_pos]
    shortest = sorted(end_distances)[0]

    return int(shortest), parents


def find_walked_steps_on_best_paths(
    end: Node,
    parents: dict[Node, set[Node]],
    target_cost: int
) -> set[Vec2i]:
    """
    Returns the set of all positions walked on all paths with total costs equal
    to the shortest path.
    Uses the subset of map node parents determined in the shortest path search.
    """
    walked_steps: set[Vec2i] = set()

    visited = set([end])
    current_path = list([end])

    def visit(node: Node, cost: int, target_cost: int) -> None:
        if cost <= target_cost:
            if node in parents:
                visited.add(node)
                for parent in parents[node]:
                    # Traversing the path backwards but adding previous nodes
                    # at the end of the list isn't a problem here as we only
                    # need them in order for determining steps between nodes
                    current_path.append(parent)
                    if parent not in visited:
                        visit(parent, cost + parent.cost, target_cost)
                    current_path.pop()
                visited.remove(node)
            else:
                for a, b in zip(current_path, current_path[1:]):
                    x_min, x_max = min(a.pos.x, b.pos.x), max(a.pos.x, b.pos.x)
                    y_min, y_max = min(a.pos.y, b.pos.y), max(a.pos.y, b.pos.y)
                    for y in range(y_min, y_max+1):
                        for x in range(x_min, x_max+1):
                            walked_steps.add(Vec2i(x, y))

    visit(end, end.cost, target_cost)

    return walked_steps


def part1(input: str) -> int:
    M: dict[Vec2i, str] = dict()

    for y, line in enumerate(input.strip().split("\n")):
        for x, m in enumerate(line):
            M[Vec2i(x, y)] = m
            if m == "S":
                start_pos = Vec2i(x, y)
            elif m == "E":
                end_pos = Vec2i(x, y)

    assert start_pos is not None
    assert end_pos is not None

    start, _, nodes, adjacencies = \
        build_graph(M, start_pos, Vec2i(1, 0), end_pos)

    shortest, _ = shortest_path_and_parents(start, nodes, end_pos, adjacencies)
    return shortest


def part2(input: str) -> int:
    M: dict[Vec2i, str] = dict()

    for y, line in enumerate(input.strip().split("\n")):
        for x, m in enumerate(line):
            M[Vec2i(x, y)] = m
            if m == "S":
                start_pos = Vec2i(x, y)
            elif m == "E":
                end_pos = Vec2i(x, y)

    assert start_pos is not None
    assert end_pos is not None

    start, end, nodes, adjacencies = \
        build_graph(M, start_pos, Vec2i(1, 0), end_pos)

    shortest, parents = \
        shortest_path_and_parents(start, nodes, end_pos, adjacencies)

    walked_positions = find_walked_steps_on_best_paths(end, parents, shortest)
    return len(walked_positions)


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day16_example1.txt", part1, 7036),
        ("Part 1", "inputs/day16_example2.txt", part1, 11048),
        ("Part 1", "inputs/day16_full.txt", part1, 122492),
        ("Part 2", "inputs/day16_example1.txt", part2, 45),
        ("Part 2", "inputs/day16_example2.txt", part2, 64),
        ("Part 2", "inputs/day16_full.txt", part2, 520),
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
