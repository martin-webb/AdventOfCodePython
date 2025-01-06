from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import Optional

YEAR = 2023
DAY = 18
NAME = "Lavaduct Lagoon"


@dataclass(eq=True, order=True, frozen=True)
class Vertex:
    x: int
    y: int


@dataclass
class Edge:
    v0: Vertex
    v1: Vertex


@dataclass
class Rect:
    v0: Vertex  # Top-left
    v1: Vertex  # Bottom-left
    v2: Vertex  # Bottom-right
    v3: Vertex  # Top-right
    el: Optional[Edge]  # Left
    eb: Optional[Edge]  # Bottom
    er: Optional[Edge]  # Right
    et: Optional[Edge]  # Top (NOTE: the top edge is the only unused one)
    width: int
    height: int


def find_rects_inside_polygon(
        vertices_to_rects: dict[Vertex, Rect],
        unique_x: list[int],
        unique_y: list[int]) -> list[Rect]:
    """
    Horizontal scanline-type approach to determining the inside-ness of all
    rects, where we use the left and right edges of each rect to determine
    polygon boundaries.
    """
    inside = []

    # NOTE Indexing rects by the top-left point so we exclude the last Y
    for y in unique_y[:-1]:
        is_in = False
        last_er = None
        # NOTE Indexing rects by the top-left point so we exclude the last X
        for x in unique_x[:-1]:
            to_add = False
            v = Vertex(x, y)
            rect = vertices_to_rects[v]

            if rect.el is not None and rect.el != last_er:
                is_in = True

            if is_in:
                to_add = True

            if is_in and rect.er is not None:
                is_in = False
                last_er = rect.er

            if to_add:
                inside.append(rect)

    return inside


def compute_total_area(
        vertices: list[Vertex],
        rects: list[Rect],
        all_vertices: set[Vertex]) -> int:
    area = 0
    for rect in rects:
        is_left_edge = rect.el is not None
        is_bottom_edge = rect.eb is not None
        is_bottom_left_corner = rect.v1 in all_vertices

        # Internal area
        # This can be zero for 2-across/2-down rect slices in which case
        # we get any area from left and bottom edges that don't lie on the
        # polygon boundary
        area += (rect.width - 2) * (rect.height - 2)

        if not is_left_edge and not is_bottom_edge:
            area += (rect.height - 1) + (rect.width - 1) - 1
            if is_bottom_left_corner:
                area -= 1
        elif not is_left_edge:
            area += (rect.height - 1)
            if is_bottom_left_corner:
                area -= 1
        elif not is_bottom_edge:
            area += (rect.width - 1)
            if is_bottom_left_corner:
                area -= 1

    perimeter = 0
    for i in range(len(vertices)):
        j = (i + 1) % len(vertices)
        v0, v1 = vertices[i], vertices[j]
        perimeter += abs(v1.x - v0.x) + abs(v1.y - v0.y)

    total = area + perimeter
    return total


def calculate_area(vertices: list[Vertex]) -> int:
    """
    """
    # All unique x and y coordinates
    unique_x_s = set()
    unique_y_s = set()
    for v in vertices:
        unique_x_s.add(v.x)
        unique_y_s.add(v.y)

    # Sort (and implicitly un-setify)
    unique_x = sorted(unique_x_s)
    unique_y = sorted(unique_y_s)

    # Determine full set of 'implicit' vertices and edges
    # Instead of just setting up the edges between v0 and v1 and using the
    # supplied vertices we want individual edges between v0 and v1 that
    # include all known X and Y vertices in-between, in other words we want
    # to instantiate all the implied edges, which are the edges that lie along
    # the polygon boundary but have only zero or one explicit vertices (two
    # explicit vertices makes an edge 'explicit')
    all_vertices = set()
    edge_points_to_edges = {}
    for i in range(len(vertices)):
        j = (i + 1) % len(vertices)
        v0, v1 = vertices[i], vertices[j]

        if v0.x == v1.x:  # Vertical edge
            all_y = [v0.y]
            for y in unique_y:
                # min() and max() because we don't know the direction of the
                # consecutive vertices (v0.x might be < or > than v1.x)
                if y > min(v0.y, v1.y) and y < max(v0.y, v1.y):
                    all_y.append(y)
            all_y.append(v1.y)
            all_y = sorted(all_y)

            for y0, y1 in zip(all_y, all_y[1:]):
                x = v0.x  # NOTE: v0.x == v1.x, we can use either here
                points = tuple(sorted([Vertex(x, y0), Vertex(x, y1)]))
                edge = Edge(v0=points[0], v1=points[1])
                edge_points_to_edges[points] = edge
                all_vertices.add(points[0])
                all_vertices.add(points[1])

        elif v0.y == v1.y:  # Horizontal edge
            all_x = [v0.x]
            for x in unique_x:
                # min() and max() because we don't know the direction of the
                # consecutive vertices (v0.x might be < or > than v1.x)
                if x > min(v0.x, v1.x) and x < max(v0.x, v1.x):
                    all_x.append(x)
            all_x.append(v1.x)
            all_x = sorted(all_x)

            for x0, x1 in zip(all_x, all_x[1:]):
                y = v0.y  # NOTE: v0.y == v1.y, we can use either here
                points = tuple(sorted([Vertex(x0, y), Vertex(x1, y)]))
                edge = Edge(v0=points[0], v1=points[1])
                edge_points_to_edges[points] = edge
                all_vertices.add(points[0])
                all_vertices.add(points[1])

    # Build sections from pairs of consecutive sorted X and Y values
    # This gives us all subdivided rectangles in the shape (both inside and
    # outside). Then we'll need to identify which are inside the polygon based
    # on a horizontal scanline-type approach
    points_to_rects = {}
    for x0, x1 in zip(unique_x, unique_x[1:]):
        for y0, y1 in zip(unique_y, unique_y[1:]):
            # Points numbered CCW from top-left
            v0 = Vertex(x=x0, y=y0)
            v1 = Vertex(x=x0, y=y1)
            v2 = Vertex(x=x1, y=y1)
            v3 = Vertex(x=x1, y=y0)

            # Polygon boundary edges for the rect
            # NOTE: These are ONLY edges that lie on the polygon boundary
            el_key = tuple(sorted((v0, v1)))
            eb_key = tuple(sorted((v1, v2)))
            er_key = tuple(sorted((v2, v3)))
            et_key = tuple(sorted((v3, v0)))

            el = edge_points_to_edges.get(el_key)
            eb = edge_points_to_edges.get(eb_key)
            er = edge_points_to_edges.get(er_key)
            et = edge_points_to_edges.get(et_key)

            rect = Rect(
                v0=v0, v1=v1, v2=v2, v3=v3,
                el=el, eb=eb, er=er, et=et,
                width=int(round(abs(v0.x - v3.x))) + 1,
                height=int(round(abs(v0.y - v1.y))) + 1
            )
            points_to_rects[v0] = rect

    rects = find_rects_inside_polygon(points_to_rects, unique_x, unique_y)
    total = compute_total_area(vertices, rects, all_vertices)
    return total


def part1(input: str) -> int:
    vertices = []
    position = (0, 0)
    for line in input.strip().split("\n"):
        direction, distance_str = line.split()[:2]
        distance = int(distance_str)

        if direction == "R":
            position = (position[0] + distance, position[1])
        elif direction == "D":
            position = (position[0], position[1] + distance)
        elif direction == "L":
            position = (position[0] - distance, position[1])
        elif direction == "U":
            position = (position[0], position[1] - distance)

        v = Vertex(x=position[0], y=position[1])
        vertices.append(v)

    total = calculate_area(vertices)
    return total


def part2(input: str) -> int:
    vertices = []
    position = (0, 0)
    direction_lookup = "RDLU"
    for line in input.strip().split("\n"):
        instruction = line.split()[2].strip("()#")
        direction = direction_lookup[int(instruction[5])]
        distance = int(instruction[:5], 16)

        if direction == "R":
            position = (position[0] + distance, position[1])
        elif direction == "D":
            position = (position[0], position[1] + distance)
        elif direction == "L":
            position = (position[0] - distance, position[1])
        elif direction == "U":
            position = (position[0], position[1] - distance)

        v = Vertex(x=position[0], y=position[1])
        vertices.append(v)

    total = calculate_area(vertices)
    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day18_example.txt", part1, 62),
        ("Part 1", "inputs/day18_full.txt", part1, 31171),
        ("Part 2", "inputs/day18_example.txt", part2, 952408144115),
        ("Part 2", "inputs/day18_full.txt", part2, 131431655002266),
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
