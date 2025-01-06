from collections import namedtuple
from pathlib import Path
from time import time
from typing import Optional

YEAR = 2023
DAY = 16
NAME = "The Floor Will Be Lava"

Node = namedtuple("Node", ["position", "char", "direction", "children"])

DIRECTIONS_TO_OFFSETS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}


def tree_build(positions_to_cells: dict,
               node: Node,
               visited: Optional[set] = None,
               depth: int = 0) -> set:
    if visited is None:
        visited = set()

    position = node.position

    visit_key = (position, node.direction)
    if visit_key in visited:
        return set()

    visited.add(visit_key)

    offset = DIRECTIONS_TO_OFFSETS[node.direction]
    while True:
        position = (position[0] + offset[0], position[1] + offset[1])
        try:
            char = positions_to_cells[position]
        except KeyError:
            break

        if char == ".":
            visited.add((position, node.direction))
        elif char == "/":
            if node.direction == "UP":
                node.children.append(Node(position, char, "RIGHT", []))
            elif node.direction == "DOWN":
                node.children.append(Node(position, char, "LEFT", []))
            elif node.direction == "LEFT":
                node.children.append(Node(position, char, "DOWN", []))
            elif node.direction == "RIGHT":
                node.children.append(Node(position, char, "UP", []))
            break
        elif char == "\\":
            if node.direction == "UP":
                node.children.append(Node(position, char, "LEFT", []))
            elif node.direction == "DOWN":
                node.children.append(Node(position, char, "RIGHT", []))
            elif node.direction == "LEFT":
                node.children.append(Node(position, char, "UP", []))
            elif node.direction == "RIGHT":
                node.children.append(Node(position, char, "DOWN", []))
            break
        elif char == "|":
            if node.direction in ("LEFT", "RIGHT"):
                node.children.append(Node(position, char, "UP", []))
                node.children.append(Node(position, char, "DOWN", []))
                break
            else:
                visited.add((position, node.direction))
        elif char == "-":
            if node.direction in ("UP", "DOWN"):
                node.children.append(Node(position, char, "LEFT", []))
                node.children.append(Node(position, char, "RIGHT", []))
                break
            else:
                visited.add((position, node.direction))

    for child in node.children:
        tree_build(positions_to_cells, child, visited, depth+1)

    return visited


def part1(input: str) -> int:
    positions_to_cells = {}

    lines = input.strip().split("\n")
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            positions_to_cells[(x, y)] = char

    root = Node((-1, 0), ".", "RIGHT", [])

    visited = tree_build(positions_to_cells, root)

    visited_positions = set(v[0] for v in visited)

    # -1 because our root node starts at (-1, 0) heading right,
    # so we can check the
    num_cells_visited = len(visited_positions) - 1
    return num_cells_visited


def part2(input: str) -> int:
    positions_to_cells = {}

    lines = input.strip().split("\n")
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            positions_to_cells[(x, y)] = char

    x_max = x
    y_max = y

    starts = []

    # Top edge - DOWN
    starts += [((x, -1), "DOWN") for x in range(x_max + 1)]
    # Bottom edge - UP
    starts += [((x, y_max + 1), "UP") for x in range(x_max + 1)]
    # Left edge - RIGHT
    starts += [((-1, y), "RIGHT") for y in range(y_max + 1)]
    # Right edge - LEFT
    starts += [((x_max + 1, y), "DOWN") for y in range(y_max + 1)]

    num_cells_visited_max = 0
    for i, (start_pos, start_dir) in enumerate(starts):
        root = Node(start_pos, ".", start_dir, [])
        visited = tree_build(positions_to_cells, root)
        visited_positions = set(v[0] for v in visited)
        # -1 because our root node starts at (-1, 0) heading right,
        # so we can check the
        num_cells_visited = len(visited_positions) - 1
        num_cells_visited_max = max(num_cells_visited_max, num_cells_visited)

    return num_cells_visited_max


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day16_example.txt", part1, 46),
        ("Part 1", "inputs/day16_full.txt", part1, 7623),
        ("Part 2", "inputs/day16_example.txt", part2, 51),
        ("Part 2", "inputs/day16_full.txt", part2, 8244),
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
