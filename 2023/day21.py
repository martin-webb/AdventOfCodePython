from collections import deque
from dataclasses import dataclass
from functools import partial
from math import floor
from time import time

YEAR = 2023
DAY = 21
NAME = "Step Counter"


@dataclass
class Plot:
    pos: tuple[int, int]
    dist: int


def distances_from(grid: dict[tuple[int, int], str],
                   start_pos: tuple[int, int]) -> dict[tuple[int, int], int]:
    """
    Return a dictionary mapping position tuples to distances from the given
    point.
    """
    distances = {}

    visited = set()
    q: deque[Plot] = deque([Plot(pos=start_pos, dist=0)])
    while q:
        candidate = q.popleft()
        if candidate.pos in visited:
            continue

        visited.add(candidate.pos)

        if grid[candidate.pos] in (".", "S"):
            distances[candidate.pos] = candidate.dist

        for o in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbour = (candidate.pos[0] + o[0], candidate.pos[1] + o[1])
            if neighbour not in grid:
                continue
            if grid[neighbour] != "#":
                q.append(Plot(pos=neighbour, dist=candidate.dist + 1))

    return distances


def num_reachable_even(grid: dict[tuple[int, int], int],
                       distance: int) -> int:
    """
    Number of even-distanced points inside (inclusive) the given distance in
    the grid.
    """
    return len([n for n in grid.values() if n <= distance and n % 2 == 0])


def num_unreachable_even(grid: dict[tuple[int, int], int],
                         distance: int) -> int:
    """
    Number of even-distanced points outside (exclusive) the given distance in
    the grid.
    """
    return len([n for n in grid.values() if n > distance and n % 2 == 0])


def num_unreachable_odd(grid: dict[tuple[int, int], int],
                        distance: int) -> int:
    """
    Number of odd-distanced points outside (exclusive) the given distance in
    the grid.
    """
    return len([n for n in grid.values() if n > distance and n % 2 == 1])


def part1(input: str, target_distance: int) -> int:
    grid = {}
    s_pos = None

    for y, row in enumerate(input.strip().split("\n")):
        for x, col in enumerate(row):
            grid[(x, y)] = col
            if col == ("S"):
                s_pos = (x, y)

    assert s_pos is not None

    # Compute tile distances with a flood fill from the starting point
    distances_from_center = distances_from(grid, s_pos)

    # Valid positions are all points even number heading back towards S
    valid_positions = [d for d in distances_from_center.values()
                       if d <= target_distance and d % 2 == 0]
    return len(valid_positions)


def part2(input: str, target_distance: int) -> int:
    grid = {}
    s_pos = None

    for y, row in enumerate(input.strip().split("\n")):
        for x, col in enumerate(row):
            grid[(x, y)] = col
            if col == ("S"):
                s_pos = (x, y)

    x_max, y_max = x, y
    width, height = x_max + 1, y_max + 1

    assert s_pos is not None
    assert width == height

    size = width
    mid = floor(size / 2)

    # Distances from the starting point
    distances_from_center = distances_from(grid, s_pos)

    # Distances from non-centre start points, one centred along each edge
    distances_for_top = distances_from(grid, (mid, y_max))
    distances_for_bottom = distances_from(grid, (mid, 0))
    distances_for_left = distances_from(grid, (x_max, mid))
    distances_for_right = distances_from(grid, (0, mid))

    # Distances from non-centre start points, one from each corner
    distances_for_top_left = distances_from(grid, (x_max, y_max))
    distances_for_top_right = distances_from(grid, (0, y_max))
    distances_for_bottom_left = distances_from(grid, (x_max, 0))
    distances_for_bottom_right = distances_from(grid, (0, 0))

    # A couple of things to clarify:
    # It's important to remember that we are considering ONLY points that are
    # reachable within EXACTLY N steps and NOT points that we pass on the way.
    # While we do trace a path over all intermediate plots for any step count,
    # the question is specifically concerned with points that are reachable AT
    # N steps exactly. This means that we have to be able to END ON a plot at
    # that step count.
    # For any point that we step off we always need an even number of steps to
    # return to it (see part 1). As the part 2 target step count is an odd
    # number then we're forced to move off any point we were on at an even step
    # count (including the starting point), however more generally an odd step
    # count would always push us off our starting point by one while an even
    # step count would allow us to return, and any 'pair' of steps taken allows
    # us to return to a previous point.
    # This means that a plot that is reachable from the start position in an
    # odd number of steps can never be reached in an even number of steps, and
    # vice versa.
    # As the map size for the full input is odd (in both directions) this means
    # that every time we cross onto a new map the 'parity' of that map flips,
    # meaning that the reachable points (the ones we can end on) are the
    # inverse of what they were before. Plots that were odd-reachable become
    # even-reachable and vice versa.
    # All of this means that for 'odd parity' maps (including the initial one)
    # we only count the number of plots reachable in an odd number and for
    # 'even parity' maps the number of plots reachable in an even number. This
    # means that the 'parity' of a map (which flips for every transition into a
    # new map) determines the steps that can be counted as reachable.
    num_odd_plots = len([
        n for n in distances_from_center.values() if n % 2 == 1])
    num_even_plots = len([
        n for n in distances_from_center.values() if n % 2 == 0])

    r = int(floor((target_distance - mid) / width))

    # NOTE: For the full input for part 2 the target distance and therefore the
    # radius is fixed and always even, however including the calculation for an
    # odd radius here to show how these are different for odd and even radii.
    num_odd_maps = r**2 if r % 2 == 1 else (r+1)**2
    num_even_maps = r**2 if r % 2 == 0 else (r+1)**2

    # The full set of reachable plots makes a diamond, which means a set of
    # fully completed maps (all reachable plots reached, above) and a set of
    # semi-complete maps (not all reachable plots reached) at the corners and
    # along the edges.
    # Start with a basic count - this includes the four partially complete
    # corner plots with odd parity and the edge plots with odd parity but
    # doesn't include the edge plots with even parity.
    basic_count = num_odd_maps * num_odd_plots + num_even_maps * num_even_plots

    # Partially complete even parity maps on the diamond edge that have not yet
    # been counted (these need to be included)
    num_edge_reachable = (
        (r * num_reachable_even(distances_for_top_left, mid - 1))
        + (r * num_reachable_even(distances_for_top_right, mid - 1))
        + (r * num_reachable_even(distances_for_bottom_left, mid - 1))
        + (r * num_reachable_even(distances_for_bottom_right, mid - 1))
    )

    # Partially complete odd parity maps on the diamond edge that have already
    # been counted as full maps (these need to be exluded)
    num_edge_unreachable = (
        ((r-1) * num_unreachable_odd(distances_for_top_left, size+mid-1))
        + ((r-1) * num_unreachable_odd(distances_for_top_right, size+mid-1))
        + ((r-1) * num_unreachable_odd(distances_for_bottom_left, size+mid-1))
        + ((r-1) * num_unreachable_odd(distances_for_bottom_right, size+mid-1))
    )

    # Partially complete odd parity maps at the corners of the diamond that
    # have already been counted as full maps (these need to be excluded)
    num_corner_unreachable = (
        num_unreachable_even(distances_for_top, size-1)
        + num_unreachable_even(distances_for_bottom, size-1)
        + num_unreachable_even(distances_for_left, size-1)
        + num_unreachable_even(distances_for_right, size-1)
    )

    num_reachable = (
        basic_count
        + num_edge_reachable
        - num_edge_unreachable
        - num_corner_unreachable
    )
    return num_reachable


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day21_example.txt",
         partial(part1, target_distance=6), 16),
        ("Part 1", "inputs/day21_full.txt",
         partial(part1, target_distance=64), 3716),
        ("Part 2", "inputs/day21_full.txt",
         partial(part2, target_distance=26501365), 616583483179597),
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
