from collections import defaultdict, deque
from dataclasses import dataclass
from functools import partial
from typing import Callable, Optional, Union, cast
from itertools import permutations
from pathlib import Path
from time import time

YEAR = 2024
DAY = 24
NAME = "Crossed Wires"


class CycleDetectedError(Exception):
    pass


@dataclass
class Input:
    value: int

    def eval(self) -> None:
        pass


@dataclass
class AND:
    value: int = 0
    p1: Optional["Gate"] = None
    p2: Optional["Gate"] = None

    def eval(self) -> None:
        assert self.p1 is not None and self.p2 is not None
        self.value = self.p1.value and self.p2.value


@dataclass
class OR:
    value: int = 0
    p1: Optional["Gate"] = None
    p2: Optional["Gate"] = None

    def eval(self) -> None:
        assert self.p1 is not None and self.p2 is not None
        self.value = self.p1.value or self.p2.value


@dataclass
class XOR:
    value: int = 0
    p1: Optional["Gate"] = None
    p2: Optional["Gate"] = None

    def eval(self) -> None:
        assert self.p1 is not None and self.p2 is not None
        self.value = self.p1.value ^ self.p2.value


@dataclass
class GateDescription:
    in_left: str
    in_right: str
    kind: str
    out: str


Gate = Union[Input | AND | OR | XOR]


GATE_TYPES = {
    "AND": AND,
    "OR": OR,
    "XOR": XOR
}


def parse_input(input: str) -> tuple[dict[str, int], list[GateDescription]]:
    """
    Parse input text and return input value map and gate descriptions.
    """
    input_strings, gate_strings = input.strip().split("\n\n")

    input_values: dict[str, int] = dict()
    for line in input_strings.split("\n"):
        label, value = line.split(": ")[0], int(line.split(": ")[1])
        input_values[label] = value

    gate_descriptions: list[GateDescription] = list()
    for line in gate_strings.split("\n"):
        parts = line.split()
        description = GateDescription(
            in_left=parts[0], in_right=parts[2], kind=parts[1], out=parts[4]
        )
        gate_descriptions.append(description)

    return input_values, gate_descriptions


def build_circuit(
    input_values: dict[str, int],
    gate_descriptions: list[GateDescription]
) -> tuple[dict[str, Gate], dict[str, set[str]], dict[str, set[str]]]:
    """
    Transform input value map and gate descriptions into a 3-tuple of gates,
    gate parents and gate children.
    """
    gates: dict[str, Gate] = dict()
    parents: dict[str, set[str]] = defaultdict(set)
    children: dict[str, set[str]] = defaultdict(set)

    # Create inputs (xNN and yNN) from initial values
    for name, value in input_values.items():
        gates[name] = Input(value)

    # First pass through gate descriptions to create the AND, OR and XOR gates
    for description in gate_descriptions:
        gate_cls = GATE_TYPES[description.kind]
        gate = gate_cls()
        gates[description.out] = cast(Gate, gate)

    # Second pass through gate descriptions to connect nodes and set up
    # parent and child adjacencies
    for description in gate_descriptions:
        in_left = gates[description.in_left]
        in_right = gates[description.in_right]
        out = gates[description.out]

        assert not isinstance(out, Input)
        out.p1 = in_left
        out.p2 = in_right

        # Save parents and children (used for analysis for part 2)
        parents[description.out].add(description.in_left)
        parents[description.out].add(description.in_right)
        children[description.in_left].add(description.out)
        children[description.in_right].add(description.out)

    return gates, parents, children


def sort_gates(gates: list[str], parents: dict[str, set[str]]) -> list[str]:
    """
    Topological sort of gates using DFS and gate parents map.
    """
    def visit(n: str, temp: set[str]) -> None:
        if n in result:
            return

        if n in temp:
            raise CycleDetectedError("Cycle detected")

        temp.add(n)
        for dependency in parents.get(n, []):
            visit(dependency, temp)
        result.append(n)

    result: list[str] = []

    unvisited = deque(gates)
    while unvisited:
        n = unvisited.popleft()
        temp: set[str] = set()
        visit(n, temp)

    return result


def find_invalid_gates(
    gates: dict[str, Gate],
    parents: dict[str, set[str]],
    children: dict[str, set[str]],
    max_bit: int,
) -> set[str]:
    """
    Analyse structure of given circuit (intended to be a Ripple-Carry Adder),
    returning a set of invalid gates (ones that are incorrect for their
    position, wired incorrectly, etc.)
    Invalid gates are determined structurally (as opposed to running specific
    inputs through the circuit and checking expected outputs on various gates).
    Specific validations/rules are limited to the checks included here (which
    were valid for my part 2 input and based on visual analysis of the circuit
    and therefore specific knowledge of the input) and so may need to be
    expanded to handle other cases in order to be more general.
    """
    invalid: set[str] = set()

    def children_by_type(n: str) -> dict[str, str]:
        """
        Returns given node's immediate childen mapped to their gate type.
        """
        return {gates[n].__class__.__name__: n for n in children[n]}

    def parents_by_type(n: str) -> dict[str, str]:
        """
        Returns given node's immediate parents mapped to their gate type.
        """
        return {gates[n].__class__.__name__: n for n in parents[n]}

    def is_z_output(n: str) -> bool:
        """
        Returns whether or not the given node is a zNN (output).
        """
        return n.startswith("z") and n[1:].isdigit()

    for bit_num in range(max_bit + 1):
        xnn = f"x{bit_num:02d}"
        ynn = f"y{bit_num:02d}"
        znn = f"z{bit_num:02d}"

        xnn_children = children_by_type(xnn)
        ynn_children = children_by_type(ynn)
        znn_parents = parents_by_type(znn)

        # Not counted as invalid (for now) but we expect these to match
        assert xnn_children == ynn_children

        # Check: Input xNN/yNN child XOR's children
        # - Grandchild XOR must be an output (zNN)
        # - Grandchild non-XOR must not be an output
        input_child_XOR_children = children_by_type(xnn_children["XOR"])
        for gate_type, name in input_child_XOR_children.items():
            if gate_type == "XOR" and not is_z_output(name):
                invalid.add(name)
            elif gate_type != "XOR" and is_z_output(name):
                invalid.add(name)

        # Check: Parents of output zNN must be AND and XOR
        if bit_num >= 2:
            if len(znn_parents) == 2:
                output_parents_list = list(znn_parents.items())
                if output_parents_list[0][0] == "AND":
                    invalid.add(output_parents_list[0][1])
                elif output_parents_list[1][0] == "AND":
                    invalid.add(output_parents_list[1][1])

        # Check: XOR grand child must be attached to the xNN output parents
        xnn_child_AND_children = children_by_type(xnn_children["AND"])
        if "AND" in xnn_child_AND_children:
            xnn_AND_grandchild = xnn_child_AND_children["AND"]
            xnn_AND_grandchild_parents = parents_by_type(xnn_AND_grandchild)
            if "XOR" not in xnn_AND_grandchild_parents:
                invalid.add(xnn_children["XOR"])

        # Check: zNN gate must be XOR
        if not isinstance(gates[znn], XOR):
            invalid.add(znn)

    return invalid


def get_bit_value(kind: str, gates: dict[str, Gate]) -> int:
    """
    Get numeric value for the xNN, yNN or zNN type gates.
    """
    values: dict[int, int] = dict()

    for name, gate in gates.items():
        if name.startswith(kind) and name[1].isdigit() and name[2].isdigit():
            num = int(name[1:])
            values[num] = gate.value

    sorted_bit_values = sorted(values.items(),
                               key=lambda item: item[0], reverse=True)
    bit_string = "".join([str(n[1]) for n in sorted_bit_values])
    return int(bit_string, 2)


def validate_swapped_wires(
    candidates: set[str],
    num_to_swap: int,
    validate_func: Callable[[int, int, int], bool],
    input_values: dict[str, int],
    gate_descriptions: list[GateDescription]
) -> set[str]:
    """
    Validates the given candidate wires to swap by generating all permutations
    of wire pairs, creating the swapped circuit and comparing the output using
    the given validation function (passed as a parameter so it can be used for
    both the example and full input in part 2).
    """
    for permutation in permutations(candidates, num_to_swap):
        updated_descriptions = list(gate_descriptions)
        for description in updated_descriptions:
            # Checks each pair to swap
            for i in range(0, len(permutation), 2):
                if description.out == permutation[i]:
                    description.out = permutation[i+1]
                elif description.out == permutation[i+1]:
                    description.out = permutation[i]

        gates, parents, _ = build_circuit(input_values, updated_descriptions)

        try:
            ordered_gates = sort_gates(list(gates.keys()), parents)
        except CycleDetectedError:
            # This is almost always an error but here we allow it to support
            # invalid swaps
            continue

        for g in ordered_gates:
            gates[g].eval()

        input_x = get_bit_value("x", gates)
        input_y = get_bit_value("y", gates)
        output_z = get_bit_value("z", gates)

        if validate_func(input_x, input_y, output_z):
            return set(gates)

    assert False, "Should not get here"


def part1(input: str) -> int:
    input_values, gate_descriptions = parse_input(input)
    gates, parents, _ = build_circuit(input_values, gate_descriptions)
    ordered_gates = sort_gates(list(gates.keys()), parents)

    for g in ordered_gates:
        gates[g].eval()

    output = get_bit_value("z", gates)
    return output


def part2_example(input: str, swapped: set[str]) -> str:
    input_values, gate_descriptions = parse_input(input)

    is_valid = validate_swapped_wires(swapped, 4,
                                      lambda a, b, c: (a & b) == c,
                                      input_values,
                                      gate_descriptions)

    assert is_valid, "Swapped wires not valid"

    result = ",".join(sorted(swapped))
    return result


def part2_full(input: str) -> str:
    input_values, gate_descriptions = parse_input(input)

    gates, parents, children = build_circuit(input_values, gate_descriptions)

    num_input_bits = max([int(n[1:])
                          for n in gates.keys()
                          if n.startswith("x") and n[1:].isdigit()])

    swapped = find_invalid_gates(gates, parents, children, num_input_bits)

    is_valid = validate_swapped_wires(swapped, 8,
                                      lambda a, b, c: (a + b) == c,
                                      input_values, gate_descriptions)

    assert is_valid, "Swapped wires not valid"

    result = ",".join(sorted(swapped))
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day24_part1_example1.txt", part1, 4),
        ("Part 1", "inputs/day24_part1_example2.txt", part1, 2024),
        ("Part 1", "inputs/day24_full.txt", part1, 53190357879014),

        ("Part 2", "inputs/day24_part2_example.txt",
         partial(part2_example, swapped=set(["z00", "z01", "z02", "z05"])),
         "z00,z01,z02,z05"),

        ("Part 2", "inputs/day24_full.txt",
         part2_full,
         "bks,hnd,nrn,tdv,tjp,z09,z16,z23"),
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
