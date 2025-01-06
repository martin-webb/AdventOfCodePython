from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from time import time

YEAR = 2023
DAY = 22
NAME = "Sand Slabs"


@dataclass(eq=True)
class Vertex:
    x: int
    y: int
    z: int


@dataclass(eq=True, frozen=True)
class Brick:
    id: int
    v0: Vertex = field(compare=False)
    v1: Vertex = field(compare=False)
    parents: set["Brick"] = field(default_factory=set, compare=False)
    children: set["Brick"] = field(default_factory=set, compare=False)


def topological_sort(bricks: list[Brick]) -> list[Brick]:
    """
    Topological sort using depth-first search. Raises an exception on detecting
    a cycle.
    """
    ordered: list[Brick] = []

    permanent = set()
    temporary = set()

    def visit(node: Brick) -> None:
        if node in temporary:
            raise ValueError("Cycle detected in graph")
        if node in permanent:
            return

        temporary.add(node)

        for child in node.children:
            visit(child)

        temporary.remove(node)
        permanent.add(node)
        ordered.insert(0, node)

    to_visit = deque(bricks)
    while to_visit:
        node = to_visit.popleft()
        visit(node)

    return ordered


def parse_bricks(input: str) -> list[Brick]:
    bricks = []

    for i, row in enumerate(input.strip().split("\n")):
        a, b = row.split("~")
        v0 = Vertex(*[int(x) for x in a.split(",")])
        v1 = Vertex(*[int(x) for x in b.split(",")])
        brick = Brick(i, v0, v1)
        bricks.append(brick)

    return bricks


def process_bricks(all_bricks: list[Brick]) -> None:
    """
    Process bricks for both parts 1 and 2.
    This does the following:
    - Updates the original bricks to have links to both their parents
      (dependencies) and children (dependents)
    - Generates a topological ordering of the bricks based on the above links
    - Settles the bricks, resulting in updated Z values for both brick vertices
    - Removes any parent-child relationships for settled bricks that are now no
      longer touching (a non-touching dependency is not a valid supporting
      brick)
    """
    # Group bricks by XY in XY-to-bricks map
    xy_to_bricks = defaultdict(list)
    for brick in all_bricks:
        for y in range(brick.v0.y, brick.v1.y + 1):
            for x in range(brick.v0.x, brick.v1.x + 1):
                xy_to_bricks[(x, y)].append(brick)

    # Sort bricks in brick lists in the XY-to-bricks map by Z-order (ascending)
    # This allows us to link each brick to both its immediate parents and
    # children.
    # Children allows us to do a depth-first search-based topological sort on
    # the brick dependency graph so we can drop bricks in the correct order.
    # Parents allows us to correctly move a brick to the lowest position it
    # would fall to based on all potential supporting bricks (potential because
    # a supporting brick may then fall lower than required to actually support
    # a dependent brick)
    for xy, bricks in xy_to_bricks.items():
        xy_to_bricks[xy] = sorted(bricks, key=lambda b: b.v0.z)

    # Link bricks to their parents and children, determining vertical
    # dependencies Determine brick vertical dependencies.
    # NOTE: This ONLY means brick pairs that are vertically dependent, and DOES
    # NOT say whether or not they'll actually be touching after falling
    for bricks in xy_to_bricks.values():
        # Each consecutive pair is a vertical/column dependency
        # NOTE: We'll inevitably end up finding duplicate parents and children
        # (as our XY-to-bricks mapping has bricks across columns) but they'll
        # only be represented once in the parent and child sets
        for parent, child in zip(bricks, bricks[1:]):
            child.parents.add(parent)
            parent.children.add(child)

    ordered = topological_sort(all_bricks)

    # Collapse bricks
    # NOTE: To account for bricks spanning multiple Z levels we always move
    # both vertices by the same offset (either towards the bottom of the tower
    # or to sit on a brick below)
    for brick in ordered:
        # Unsupported bricks (no parents) fall to the bottom (Z value 1)
        if len(brick.parents) == 0:
            offset = 1 - min(brick.v0.z, brick.v1.z)
            brick.v0.z += offset
            brick.v1.z += offset
        else:
            # As a brick can have multiple supports we can only drop this brick
            # down to sit on top of the support with the highest Z value (being
            # sure to take into account both vertices)
            max_z = 0
            for parent in brick.parents:
                max_z = max(max_z, parent.v0.z, parent.v1.z)
            z_offset = max_z - min(brick.v0.z, brick.v1.z) + 1
            brick.v0.z += z_offset
            brick.v1.z += z_offset

    # Remove parent-child dependencies between bricks that after settling are
    # now not touching.
    # NOTE: We don't need to update the topological order as this won't change,
    # this will only remove a subset of the direct dependencies.
    # NOTE: We can also apply the bricks-must-touch constraint when we actually
    # process the bricks (for the part 1 and 2 requirements), but doing it here
    # gives us a structure we can use for both.
    for brick in ordered:
        for child in set(brick.children):  # Copy as we need to mutate the set
            # Skip child if not touching as (after settling) the child doesn't
            # count as a dependency because it must be supported by one or more
            # other bricks
            z_diff = min(child.v0.z, child.v1.z) - max(brick.v0.z, brick.v1.z)
            if z_diff > 1:
                brick.children.remove(child)
                child.parents.remove(brick)


def part1(input: str) -> int:
    all_bricks = parse_bricks(input)

    process_bricks(all_bricks)

    num_safe_to_disintegrate = 0
    for brick in all_bricks:
        is_safe = True

        # ALL children must have >= 2 parents, so a single child without makes
        # this brick unsafe to disintegrate
        for child in brick.children:
            if len(child.parents) < 2:
                is_safe = False
                # No need to check any more as ALL children must have two or
                # more parents
                break

        if is_safe:
            num_safe_to_disintegrate += 1

    return num_safe_to_disintegrate


def part2(input: str) -> int:
    all_bricks = parse_bricks(input)

    process_bricks(all_bricks)

    sum_of_other_bricks_to_fall = 0
    for brick in all_bricks:
        to_visit = deque([brick])
        deleted = set()
        while to_visit:
            current = to_visit.popleft()
            deleted.add(current)
            for child in current.children:
                for parent in child.parents:
                    # Found a parent node that hasn't been disintegrated?
                    # This child is safe and we don't need to search any
                    # further down these brick dependencies
                    if parent not in deleted:
                        break
                else:
                    # Otherwise, all parents of this child have been deleted so
                    # it will disintegrate and we need to then check its own
                    # children
                    to_visit.append(child)
        sum_of_other_bricks_to_fall += len(deleted) - 1

    return sum_of_other_bricks_to_fall


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day22_example.txt", part1, 5),
        # ("Part 1", "inputs/day22_custom1.txt", part1, 3),
        # ("Part 1", "inputs/day22_custom2.txt", part1, 2),
        ("Part 1", "inputs/day22_full.txt", part1, 446),
        ("Part 2", "inputs/day22_example.txt", part2, 7),
        ("Part 2", "inputs/day22_full.txt", part2, 60287),
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
