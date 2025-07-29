from collections import defaultdict, deque
from io import StringIO
from itertools import chain, combinations, pairwise
from pathlib import Path
import re
import sys
from time import time

YEAR = 2016
DAY = 11
NAME = "Radioisotope Thermoelectric Generators"

GENERATOR_PATTERN = r"([a-z]+ generator)"
MICROCHIP_PATTERN = r"([a-z]+-compatible microchip)"


def parse_input(input: str) -> dict[str, int]:
    floors: dict[str, int] = dict()

    # XXX: Assumes 1-based floor numbering and input in ascending floor order
    for i, line in enumerate(input.strip().split("\n"), start=1):
        generators = re.findall(GENERATOR_PATTERN, line)
        microchips = re.findall(MICROCHIP_PATTERN, line)

        for generator in generators:
            label = f"{generator[0]}G".upper()
            floors[label] = i

        for microchip in microchips:
            label = f"{microchip[0]}M".upper()
            floors[label] = i

    return floors


def draw(floors: dict[str, int], destination: int) -> str:
    """
    Visualise the building.
    """
    buf = StringIO()

    # Assign each object a unique column (sorted for consistency)
    # We add 'E' manually so it's always first
    object_column_indices = {"E": 0}
    object_column_indices.update({
        x: i
        for i, x in enumerate(sorted(floors.keys()), start=1)
        if x != "E"
    })

    # Map each object to a (col, floor) position based on its actual floor and
    # the column assignment
    grid = {(object_column_indices[o], n): o for o, n in floors.items()}

    x_max = max(object_column_indices.values())
    y_max = destination
    col_width = 3

    buf.write("---" * (x_max + 2))
    buf.write("\n")

    for y in range(y_max, 0, -1):
        buf.write(f"F{y}".ljust(col_width))
        for x in range(x_max+1):
            if (x, y) in grid:
                buf.write(grid[(x, y)].ljust(col_width))
            else:
                buf.write(".".ljust(col_width))
        buf.write("\n")

    buf.write("---" * (x_max + 2))
    buf.write("\n")

    return buf.getvalue()


def is_safe(floors: dict[str, int]) -> bool:
    """
    >>> is_safe({"HG": 1, "HM": 1})
    True
    >>> is_safe({"HG": 1, "HM": 2})
    True
    >>> is_safe({"HG": 1, "HM": 1, "LG": 1, "LM": 1})
    True
    >>> is_safe({"HG": 1, "HM": 1, "LG": 2, "LM": 1})
    False
    >>> is_safe({"HG": 2, "HM": 1, "LG": 1, "LM": 2})
    False
    >>> is_safe({"HG": 1, "HM": 2, "LG": 3, "LM": 1})
    False
    """
    num_fried = 0

    generators_by_floor = defaultdict(set)
    microchips_by_floor = defaultdict(set)

    for k, v in floors.items():
        if k.endswith("G"):
            generators_by_floor[v].add(k)
        if k.endswith("M"):
            microchips_by_floor[v].add(k)

    # Removes pairs of matching generators and microchips and checks for any
    # remaining microchips where there is at least one generator
    for floor_num, microchips in microchips_by_floor.items():
        unpaired_microchips = set(microchips)

        for microchip in microchips:
            equivalent_generator = f"{microchip[0]}G"
            if equivalent_generator in generators_by_floor[floor_num]:
                unpaired_microchips.remove(microchip)

        # No generator? No problem
        if len(generators_by_floor[floor_num]) > 0:
            num_fried += len(unpaired_microchips)

    return num_fried == 0


def find_min_steps(start: dict[str, int], destination: int) -> int:
    """
    Bread-first search to find the minimum number of steps to get all objects
    to the destination floor.
    """
    min_found = sys.maxsize

    num_objects_on_current_floor = len({
        k: v for k, v in start.items() if v == start["E"] and k != "E"
    })

    assert num_objects_on_current_floor != 0, \
        "Unsolvable (no objects on same floor as elevator)"

    # We need to avoid revisiting previous states as the elevator can make
    # movements that undo previous ones. This can happen over more than a
    # single time step, so we're not just looking to prevent individual
    # reversals of the previous movement but avoid any previous state.
    visited = set()

    Q: deque[tuple[dict[str, int], int]] = deque([(start, 0)])
    while Q:
        floors, total_steps = Q.popleft()

        visited_key = tuple(sorted(floors.items()))
        visited.add(visited_key)

        all_at_destination = all([(n == destination) for n in floors.values()])
        if all_at_destination:
            min_found = min(min_found, total_steps)
            continue

        current_floor = floors["E"]

        # Only looking at the floor with the elevator
        objects_on_current_floor = set(
            [k for k, v in floors.items() if v == current_floor and k != "E"]
        )

        # We can move one or two items on the elevator at the same time.
        # XXX: We prioritise moving as many objects at a time as possible so
        # test movements with pairs of objects first. In theory this seems like
        # it might help with search speed but in practice with the puzzle
        # inputs this doesn't seem to make much of a difference.
        # FIXME: If we have to go down we might also prefer moving as _few_
        # objects as possible to avoid undoing progress, however given that
        # preferring moving more objects doesn't seem to make much difference
        # on these input sizes this may not help that much.
        movement_combinations = list(chain(
            combinations(objects_on_current_floor, 2),
            combinations(objects_on_current_floor, 1)
        ))

        for movement_combination in movement_combinations:
            # Determine the minimum intermediate destination floor which is the
            # current lowest floor value, as we never need to go back down to a
            # floor below that.
            min_floor = min(floors.values())

            # Additionally, if the object movement removes all objects from the
            # current floor we also don't need to consider this now-empty floor
            # as a candidate minimum. This allows us to prune the search space
            # a bit and cuts the search time roughly in half.
            num_objects_on_current_floor = len(objects_on_current_floor)
            num_objects_moved = len(movement_combination)
            if num_objects_on_current_floor - num_objects_moved == 0:
                min_floor += 1

            for next_floor in range(destination, min_floor-1, -1):
                if next_floor == current_floor:
                    continue

                candidate = dict(floors)
                candidate["E"] = next_floor

                for o in movement_combination:
                    candidate[o] = next_floor

                candidate_key = tuple(sorted(candidate.items()))
                if candidate_key in visited:
                    continue

                if not is_safe(candidate):
                    continue

                steps = abs(next_floor - current_floor)
                Q.append((candidate, total_steps + steps))

    return min_found


def solve(floors: dict[str, int], begin: int, destination: int) -> int:
    """
    We can do this efficiently with a breadth-first search for the minimum by
    only considering just two pairs of generator and microchip combinations at
    the same time and always moving them all to the top floor.

    As we always need at least one microchip or generator to move the elevator,
    we must make sure that at least one generator or microchip from the first
    two pairs is on the starting floor with the elevator (the bottom floor), as
    otherwise we won't be able to move.

    With the first pair done, the elevator will then always be at the top floor
    at the end and by re-using either of the previous pairs from before and
    picking a new pair we can then solve with the new pair, repeating this with
    each additional pair until we're done, with the elevator always ending at
    the top floor along with the new pairs.

    For example, if the elements were as follows:
    A, B, C, D, E
    We could solve with the following pairings (assuming that A or B contains
    at least one generator or microchip on the starting floor):
    (A,B), (B,C), (C,D), (D,E)
    """
    result = 0

    # Add elevator so we can actually move
    floors.update({"E": begin})

    # Use these to divide the floors into separate generator and microchip
    # element combinations to solve for
    all_elements = set(k[0] for k in floors.keys())

    # Enforce basic solvability requirement:
    # This ensures that we have at least one object on the floor we start on,
    # as the elevator requires at least one object to move, so we need to make
    # sure the first couple of pairs we take satisifies this requirement
    elements_on_start_floor = set(
        k[0] for k, v in floors.items() if v == begin
    )
    elements_remaining = all_elements - elements_on_start_floor
    elements = list(elements_on_start_floor) + list(elements_remaining)

    # Solve with just two pairs at a time (a generator and microchip for each,
    # plus of course the elevator)
    for pair in pairwise(elements):
        E = "E"
        AM = f"{pair[0]}M"
        AG = f"{pair[0]}G"
        BM = f"{pair[1]}M"
        BG = f"{pair[1]}G"

        # Subset of generators and microchips to consider for this iteration
        subset = {k: v
                  for k, v in floors.items()
                  if k in set([AM, AG, BM, BG, E])}

        min_steps = find_min_steps(subset, destination)

        # XXX: Assumes that the result of find_min_steps() is a successful move
        # of all objects to the top floor
        floors.update({
            AG: destination,
            AM: destination,
            BG: destination,
            BM: destination,
            E: destination
        })

        result += min_steps

    return result


def part1(input: str) -> int:
    floors = parse_input(input)
    min_steps = solve(floors, 1, 4)
    return min_steps


def part2(input: str) -> int:
    floors = parse_input(input)

    new = {"EG": 1, "EM": 1, "DG": 1, "DM": 1}

    # XXX: These letters MUST NOT clash with the input
    for k in new.keys():
        assert k not in floors

    floors.update(new)

    min_steps = solve(floors, 1, 4)
    return min_steps


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day11_full.txt", part1, 37),
        ("Part 2", "inputs/day11_full.txt", part2, 61),
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
