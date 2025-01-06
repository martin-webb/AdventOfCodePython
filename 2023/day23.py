from dataclasses import dataclass, field
from time import time
from typing import Optional

YEAR = 2023
DAY = 23
NAME = "A Long Walk"


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Node:
    id: int
    point: Point


@dataclass(frozen=True)
class Edge:
    begin: Node
    end: Node
    distance: int


@dataclass
class Graph:
    points_to_nodes: dict[Point, Node] = field(default_factory=dict)
    edges: dict[Node, list[Edge]] = field(default_factory=dict)

    def add_node(self, node: Node) -> None:
        self.points_to_nodes[node.point] = node

    def add_edge(self, edge: Edge) -> None:
        if edge.begin not in self.edges:
            self.edges[edge.begin] = list()
        self.edges[edge.begin].append(edge)


def find_start_and_end_points(grid: dict[Point, str]) -> tuple[Point, Point]:
    """
    Find the start and end points in the map in the top and bottom rows.
    """
    x_max = max(xy.x for xy in grid.keys())
    y_max = max(xy.y for xy in grid.keys())

    for x in range(x_max + 1):
        point_top = Point(x, 0)
        point_bottom = Point(x, y_max)

        if grid[point_top] == ".":
            start_pos = point_top
        if grid[point_bottom] == ".":
            end_pos = point_bottom

    return (start_pos, end_pos)


def distance_to_next_node(
        grid: dict[Point, str],
        node_points: set[Point],
        current: Point,
        previous: Point,
        valid_up: set[str],
        valid_down: set[str],
        valid_left: set[str],
        valid_right: set[str]) -> Optional[tuple[Point, int]]:
    """
    Find the next crossing point from the given starting point, moving in the
    direction determined by the combination of the current and previous points.
    """
    distance = 1

    while True:
        found_node = current in node_points
        if found_node:
            break

        up = Point(current.x, current.y - 1)
        down = Point(current.x, current.y + 1)
        left = Point(current.x - 1, current.y)
        right = Point(current.x + 1, current.y)

        if up != previous and grid.get(up) in valid_up:
            current, previous = up, current
        elif down != previous and grid.get(down) in valid_down:
            current, previous = down, current
        elif left != previous and grid.get(left) in valid_left:
            current, previous = left, current
        elif right != previous and grid.get(right) in valid_right:
            current, previous = right, current
        else:
            return None

        distance += 1

    return (current, distance)


def find_nodes(
        grid: dict[Point, str], x_max: int, y_max: int, graph: Graph) -> None:
    """
    Find crossing points in the map (nodes) and add them to the graph.
    """
    next_id_pow = 0

    for y in range(y_max + 1):
        for x in range(x_max + 1):
            point = Point(x, y)
            tile = grid[point]
            if tile == "#":
                continue

            num_neighbouring_paths = 0

            up = grid.get(Point(x, y - 1))
            down = grid.get(Point(x, y + 1))
            left = grid.get(Point(x - 1, y))
            right = grid.get(Point(x + 1, y))

            valid = {".", "^", "v", "<", ">"}
            if up in valid:
                num_neighbouring_paths += 1
            if down in valid:
                num_neighbouring_paths += 1
            if left in valid:
                num_neighbouring_paths += 1
            if right in valid:
                num_neighbouring_paths += 1

            # One neighbouring path for a start or end node, two for any point
            # along a path BETWEEN nodes, three or more for nodes with multiple
            # exits
            if num_neighbouring_paths == 1 or num_neighbouring_paths >= 3:
                node = Node(id=2**next_id_pow, point=point)
                next_id_pow += 1
                graph.add_node(node)


def find_edges(grid: dict[Point, str],
               graph: Graph,
               valid_up: set[str],
               valid_down: set[str],
               valid_left: set[str],
               valid_right: set[str]) -> None:
    """
    Find paths (edges) between crossing points (nodes) in the map and add them
    to the graph.
    """
    # Lookup set for nodes
    node_points = set(graph.points_to_nodes.keys())

    for node in graph.points_to_nodes.values():
        up = Point(node.point.x, node.point.y - 1)
        down = Point(node.point.x, node.point.y + 1)
        left = Point(node.point.x - 1, node.point.y)
        right = Point(node.point.x + 1, node.point.y)

        if grid.get(up) in valid_up:
            result = distance_to_next_node(
                grid, node_points, up, node.point,
                valid_up, valid_down, valid_left, valid_right)
            if result is not None:
                begin = node
                end = graph.points_to_nodes[result[0]]
                distance = result[1]
                edge = Edge(begin, end, distance)
                graph.add_edge(edge)

        if grid.get(down) in valid_down:
            result = distance_to_next_node(
                grid, node_points, down, node.point,
                valid_up, valid_down, valid_left, valid_right)
            if result is not None:
                begin = node
                end = graph.points_to_nodes[result[0]]
                distance = result[1]
                edge = Edge(begin, end, distance)
                graph.add_edge(edge)

        if grid.get(left) in valid_left:
            result = distance_to_next_node(
                grid, node_points, left, node.point,
                valid_up, valid_down, valid_left, valid_right)
            if result is not None:
                begin = node
                end = graph.points_to_nodes[result[0]]
                distance = result[1]
                edge = Edge(begin, end, distance)
                graph.add_edge(edge)

        if grid.get(right) in valid_right:
            result = distance_to_next_node(
                grid, node_points, right, node.point,
                valid_up, valid_down, valid_left, valid_right)
            if result is not None:
                begin = node
                end = graph.points_to_nodes[result[0]]
                distance = result[1]
                edge = Edge(begin, end, distance)
                graph.add_edge(edge)


def build_graph(grid: dict[Point, str],
                x_max: int,
                y_max: int,
                valid_up: set[str],
                valid_down: set[str],
                valid_left: set[str],
                valid_right: set[str]) -> Graph:
    """
    Build graph structure (nodes and edges) from map.
    """
    graph = Graph()

    find_nodes(grid, x_max, y_max, graph)
    find_edges(grid, graph, valid_up, valid_down, valid_left, valid_right)

    return graph


def find_paths(graph: Graph, src: Node, dst: Node) -> list[int]:
    """
    Find end nodes in graph with depth first search traversal.
    """
    def _find_paths(src: Node, visited: int, distance: int) -> None:
        """
        Recursive DFS implementation.
        """
        if src.id == dst.id:
            distances.append(distance)
        else:
            visited |= src.id
            for edge in graph.edges[src]:
                if not (visited & edge.end.id):
                    _find_paths(edge.end, visited, distance + edge.distance)

    distances: list[int] = list()
    _find_paths(src, 0, 0)
    return distances


def prune_graph(graph: Graph, start: Node, end: Node) -> None:
    """
    Remove any nodes or edges from that graph that aren't required for this.
    """
    if end in graph.edges:
        # If there are edges heading away from the end node (for these puzzle
        # inputs this only happens with the part two change allowing moving up
        # slopes), then we can remove any edge from a pre-end node that doesn't
        # move to the end node, as the requirement that we never touch the same
        # tile twice means we could never cross that node again to get to the
        # end, so that entire path isn't worth checking
        # This reduces the run time for this from ~30s to ~18s
        nodes_before_end = [edge.end for edge in graph.edges[end]]
        for node_before_end in nodes_before_end:
            edges_to_remove = []
            for edge in graph.edges[node_before_end]:
                if edge.end != end:
                    edges_to_remove.append(edge)
            for edge in edges_to_remove:
                graph.edges[node_before_end].remove(edge)


def part1(input: str) -> int:
    grid = {}

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            grid[Point(x, y)] = char

    x_max, y_max = x, y

    # Set of tiles that are allowed for movement in each direction
    valid_up = {".", "^"}
    valid_down = {".", "v"}
    valid_left = {".", "<"}
    valid_right = {".", ">"}

    graph = build_graph(
        grid, x_max, y_max, valid_up, valid_down, valid_left, valid_right)

    start_p, end_p = find_start_and_end_points(grid)
    start = graph.points_to_nodes[start_p]
    end = graph.points_to_nodes[end_p]

    prune_graph(graph, start, end)

    distances = find_paths(graph, start, end)

    longest = max(distances)
    return longest


def part2(input: str) -> int:
    grid = {}

    for y, line in enumerate(input.strip().split("\n")):
        for x, char in enumerate(line):
            grid[Point(x, y)] = char

    x_max, y_max = x, y

    # Set of tiles that are allowed for movement in each direction
    # Part 2 essentially allows movement up slopes
    # NOTE: An alternative approach would be to rewrite the map when parsed
    valid_up = {".", "^", "v", "<", ">"}
    valid_down = {".", "^", "v", "<", ">"}
    valid_left = {".", "^", "v", "<", ">"}
    valid_right = {".", "^", "v", "<", ">"}

    graph = build_graph(
        grid, x_max, y_max, valid_up, valid_down, valid_left, valid_right)

    start_p, end_p = find_start_and_end_points(grid)
    start = graph.points_to_nodes[start_p]
    end = graph.points_to_nodes[end_p]

    prune_graph(graph, start, end)

    distances = find_paths(graph, start, end)

    longest = max(distances)
    return longest


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day23_example.txt", part1, 94),
        ("Part 1", "inputs/day23_full.txt", part1, 2130),
        ("Part 2", "inputs/day23_example.txt", part2, 154),
        ("Part 2", "inputs/day23_full.txt", part2, 6710),
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
