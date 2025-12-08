from itertools import combinations
from dataclasses import dataclass
from functools import partial
from math import dist
from pathlib import Path
from time import time

YEAR = 2025
DAY = 8
NAME = "Playground"


@dataclass(frozen=True, order=True)
class Vec3:
    x: int
    y: int
    z: int

    def euclidian_distance(self, other: "Vec3") -> float:
        distance = dist((self.x, self.y, self.z), (other.x, other.y, other.z))
        return distance


def parse_input(input: str) -> list[Vec3]:
    boxes: list[Vec3] = list()

    for line in input.strip().split("\n"):
        x, y, z = line.split(",")
        box = Vec3(int(x), int(y), int(z))
        boxes.append(box)

    return boxes


def compute_sorted_distances_for_pairs(
    boxes: list[Vec3]
) -> list[tuple[float, tuple[Vec3, Vec3]]]:
    distances_with_pairs: list[tuple[float, tuple[Vec3, Vec3]]] = list()

    for a, b in combinations(boxes, 2):
        d = a.euclidian_distance(b)
        distances_with_pairs.append((d, (a, b)))

    sorted_distances_with_pairs = sorted(distances_with_pairs,
                                         key=lambda x: x[0])
    return sorted_distances_with_pairs


def connect_junction_boxes(
    boxes: tuple[Vec3, Vec3],
    _circuits: list[set[Vec3]],
    _boxes_to_circuits: dict[Vec3, int]
) -> tuple[list[set[Vec3]], dict[Vec3, int], int]:
    """
    Connect the two junction boxes, updating copies of the circuits sets and
    the box-to-circuits ID map.
    """
    # Updatable copies and extra information to return
    circuits = list(_circuits)
    boxes_to_circuits = dict(_boxes_to_circuits)
    num_merged = 0

    # Check no self-connections
    assert boxes[0] != boxes[1]

    box_0_circuit = boxes_to_circuits.get(boxes[0])
    box_1_circuit = boxes_to_circuits.get(boxes[1])

    # Both junction boxes assigned to circuits/groups (merge *might* happen)
    if box_0_circuit is not None and box_1_circuit is not None:
        # Merge two separate circuits
        if box_0_circuit != box_1_circuit:
            assert circuits[box_0_circuit].isdisjoint(circuits[box_1_circuit])
            # Update membership for A
            circuits[box_0_circuit].update(circuits[box_1_circuit])

            # Reassign membership for elements in B
            for elem in circuits[box_1_circuit]:
                boxes_to_circuits[elem] = box_0_circuit

            # Clear old membership
            circuits[box_1_circuit].clear()

            num_merged += 1

    # One junction box assigned to a circuit/group (left)
    elif box_0_circuit is not None and box_1_circuit is None:
        boxes_to_circuits[boxes[1]] = box_0_circuit
        circuits[box_0_circuit].add(boxes[1])
        num_merged += 1

    # One junction box assigned to a circuit/group (right)
    elif box_0_circuit is None and box_1_circuit is not None:
        boxes_to_circuits[boxes[0]] = box_1_circuit
        circuits[box_1_circuit].add(boxes[0])
        num_merged += 1

    # New circuit/group for both
    elif box_0_circuit is None and box_1_circuit is None:
        circuits.append(set([boxes[0], boxes[1]]))
        circuit_id = len(circuits) - 1
        boxes_to_circuits[boxes[0]] = circuit_id
        boxes_to_circuits[boxes[1]] = circuit_id
        num_merged += 1

    else:
        assert False, "Should not get here"

    return circuits, boxes_to_circuits, num_merged


def part1(input: str, target_connections: int) -> int:
    boxes = parse_input(input)
    distances_with_pairs = compute_sorted_distances_for_pairs(boxes)

    circuits: list[set[Vec3]] = list()
    boxes_to_circuits: dict[Vec3, int] = dict()

    for _, box_pairs in distances_with_pairs[:target_connections]:
        circuits, boxes_to_circuits, _ = \
            connect_junction_boxes(box_pairs, circuits, boxes_to_circuits)

    circuits_by_size = sorted(circuits, key=lambda c: len(c), reverse=True)
    top_3_lengths = [len(c) for c in circuits_by_size[:3]]
    result = top_3_lengths[0] * top_3_lengths[1] * top_3_lengths[2]
    return result


def part2(input: str) -> int:
    boxes = parse_input(input)
    distances_with_pairs = compute_sorted_distances_for_pairs(boxes)

    circuits: list[set[Vec3]] = list()
    boxes_to_circuits: dict[Vec3, int] = dict()
    num_circuits = len(boxes)

    result = None

    for _, box_pairs in distances_with_pairs:
        circuits, boxes_to_circuits, num_merged = \
            connect_junction_boxes(box_pairs, circuits, boxes_to_circuits)
        num_circuits -= num_merged
        if num_circuits == 1:
            result = box_pairs[0].x * box_pairs[1].x
            break

    assert result is not None
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day08_example.txt",
         partial(part1, target_connections=10), 40),
        ("Part 1", "inputs/day08_full.txt",
         partial(part1, target_connections=1000), 50760),
        ("Part 2", "inputs/day08_example.txt", part2, 25272),
        ("Part 2", "inputs/day08_full.txt", part2, 3206508875),
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
