from collections import deque
from dataclasses import dataclass
from pathlib import Path
from time import time

YEAR = 2016
DAY = 22
NAME = "Grid Computing"


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    size: int
    used: int
    avail: int


def parse_node_line(s: str) -> Node:
    parts = s.split()
    basename = parts[0].split("/")[-1]
    name_parts = basename.split("-")
    x = int(name_parts[1].strip("x"))
    y = int(name_parts[2].strip("y"))
    size = int(parts[1].strip("T"))
    used = int(parts[2].strip("T"))
    avail = int(parts[3].strip("T"))
    node = Node(x=x, y=y, size=size, used=used, avail=avail)
    return node


def parse_input(input: str) -> dict[tuple[int, int], Node]:
    nodes: dict[tuple[int, int], Node] = dict()

    lines = input.strip().split("\n")
    for line in lines[2:]:
        node = parse_node_line(line)
        nodes[(node.x, node.y)] = node

    return nodes


def part1(input: str) -> int:
    nodes = parse_input(input)

    num_viable_pairs = 0

    for a in nodes.values():
        for b in nodes.values():
            if a == b:
                continue
            if a.used == 0:
                continue
            if a.used <= b.avail:
                num_viable_pairs += 1

    return num_viable_pairs


def distances_from(
        nodes: dict[tuple[int, int], Node],
        start_pos: tuple[int, int],
        ) -> dict[tuple[int, int], int]:
    """
    Breadth-first flood fill to find distances to other nodes starting from the
    given position, taking into account the requirement that the current total
    size must accomodate the neighbour node used size (with complete data swaps
    allowing us to simply move blocks in their entirety).
    """
    distances: dict[tuple[int, int], int] = dict()

    visited: set[tuple[int, int]] = set()

    q: deque[tuple[tuple[int, int], int]] = deque([(start_pos, 0)])
    while q:
        current, distance = q.popleft()
        distances[current] = distance

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for direction in directions:
            neighbour = (current[0] + direction[0], current[1] + direction[1])
            if neighbour in visited:
                continue
            if neighbour not in nodes:
                continue

            # We must have enough space to swap
            current_node = nodes[current]
            neighbour_node = nodes[neighbour]
            if neighbour_node.used > current_node.size:
                continue

            q.append((neighbour, distance+1))
            visited.add(neighbour)

    return distances


def part2(input: str) -> int:
    """
    Insights:
    1. As we can only move an entire node's data in one swap, we don't have a
    search space that involves moving partial data onto multiple nodes and
    constantly revisiting nodes based on newly-available free space. We can
    simply use the current total size and neighbour used sizes to determine the
    viability of any swap.
    2. We can do the entire thing non-simulated with just source-to-destination
    node distances and some known movement patterns, without needing to
    simulate the actual swaps.
    3. From visualisation of the puzzle input, our grid has a 'wall' we need to
    move around as we swap for part 1 (see below).

    There are three parts to the non-simulated solution:
    1. Bring the empty node adjacent to the goal, avoiding any 'walls' in our
    puzzle input (breadth-first flood fill to find shortest distances), to get
    our free node to one position away from the goal node.

    2. From that position repeatedly execute five-step swaps ('hooking' the
    goal node) until our current free node position is at the destination node
    and the goal node is one position away.
    NOTE: This assumes we can always 'hook' in a 2x3 or 3x2 grid to get to the
    end, we're not blocked, and each hook movement is always five steps.
    The repeated five-step 'hook' movement here moves the goal node one
    position and looks like the following:
    . _ G -> . G _ -> . G . -> . G . -> . G . -> _ G .
    . . .    . . .    . . _    . _ .    _ . .    . . .

    3. Do one more final move to swap our free node from the destination with
    the adjacent goal node, to get the goal node to the destination.
    This final move simply looks like following:
    _ G -> G _
    . .    . .
    """
    nodes = parse_input(input)

    # There's just one valid starting node (in our puzzle input)
    empty_nodes = [node for node in nodes.values() if node.used == 0]
    assert len(empty_nodes) == 1, \
        f"Wanted 1 free node, got {len(empty_nodes)}"

    start_node = empty_nodes[0]
    assert start_node.used == 0, \
        f"Wanted empty start node, got {start_node.used}"

    max_x = max(node.x for node in nodes.values())
    goal_node = nodes[(max_x, 0)]

    start_pos = (start_node.x, start_node.y)
    end_adjacent_pos = (1, 0)
    goal_pos = (goal_node.x, goal_node.y)
    goal_adjacent_pos = (goal_pos[0] - 1, goal_pos[1])

    min_steps = 0

    # Part 1
    distances_from_start = distances_from(nodes, start_pos)
    min_steps += distances_from_start[goal_adjacent_pos]

    # Part 2
    distances_from_goal = distances_from(nodes, goal_pos)
    min_steps += distances_from_goal[end_adjacent_pos] * 5

    # Part 3
    min_steps += 1

    return min_steps


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day22_full.txt", part1, 1024),
        ("Part 2", "inputs/day22_example.txt", part2, 7),
        ("Part 2", "inputs/day22_full.txt", part2, 230),
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
