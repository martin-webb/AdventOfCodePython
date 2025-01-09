from collections import defaultdict, deque
from collections.abc import Callable, Iterable
from pathlib import Path
from time import time

YEAR = 2015
DAY = 7
NAME = "Some Assembly Required"


def make_binary_operator(kind: str, op1: str, op2: str) -> Callable:
    if kind == "AND":
        def f(op1: str, op2: str) -> Callable:
            def eval(values: dict[str, int]) -> int:
                return (values[op1] & values[op2]) & 0xFFFF
            return eval
        return f(op1, op2)

    elif kind == "OR":
        def f(op1: str, op2: str) -> Callable:
            def eval(values: dict[str, int]) -> int:
                return (values[op1] | values[op2]) & 0xFFFF
            return eval
        return f(op1, op2)

    elif kind == "LSHIFT":
        def f(op1: str, op2: str) -> Callable:
            def eval(values: dict[str, int]) -> int:
                return (values[op1] << values[op2]) & 0xFFFF
            return eval
        return f(op1, op2)

    elif kind == "RSHIFT":
        def f(op1: str, op2: str) -> Callable:
            def eval(values: dict[str, int]) -> int:
                return (values[op1] >> values[op2]) & 0xFFFF
            return eval
        return f(op1, op2)

    assert False, "Should not get here"


def make_unary_operator(kind: str, op: str) -> Callable:
    if kind == "NOT":
        def f(op: str) -> Callable:
            def eval(values: dict[str, int]) -> int:
                return ~values[op] & 0xFFFF
            return eval
        return f(op)

    assert False, "Should not get here"


def make_value_operator(op: str) -> Callable:
    def f(op: str) -> Callable:
        def eval(values: dict[str, int]) -> int:
            # Works for both "0 -> b" and "a -> b".
            if op.isdigit():
                return int(op) & 0xFFFF
            else:
                return values[op] & 0xFFFF
        return eval
    return f(op)


def parse_input(input: str) -> tuple[dict[str, Callable], dict[str, set[str]]]:
    """
    Parse circuit input and return a pair containing:
    - A map of wire names to callables that can be called to return the value
      for that specific wire
    - A map of wire dependencies (used for topological sort on the wires for
      correct evaluation order)
    """
    wires: dict[str, Callable] = dict()
    dependencies: dict[str, set[str]] = defaultdict(set)

    for line in input.strip().split("\n"):
        parts = line.split()
        if len(parts) == 5:  # AND, OR, LSHIFT, RSHIFT
            op1, operator, op2, name = parts[0], parts[1], parts[2], parts[4]

            if op1.isdigit():
                if op1 not in wires:
                    wires[op1] = make_value_operator(op1)

            if op2.isdigit():
                if op2 not in wires:
                    wires[op2] = make_value_operator(op2)

            wires[name] = make_binary_operator(operator, op1, op2)
            dependencies[name].add(op1)
            dependencies[name].add(op2)

        elif len(parts) == 4:  # NOT
            operator, op1, name = parts[0], parts[1], parts[3]
            if op1.isdigit():
                if op1 not in wires:
                    wires[op1] = make_value_operator(op1)

            wires[name] = make_unary_operator(operator, op1)
            dependencies[name].add(op1)

        elif len(parts) == 3:  # Value
            op1, name = parts[0], parts[2]
            if op1.isdigit():
                if op1 not in wires:
                    wires[op1] = make_value_operator(op1)

            wires[name] = make_value_operator(op1)
            dependencies[name].add(op1)

    return wires, dependencies


def sort_wires(
    wires: Iterable[str],
    dependencies: dict[str, set[str]]
) -> list[str]:
    """
    Topological sort of wires using DFS and wire dependencies map.
    """
    def visit(n: str, temp: set[str]) -> None:
        if n in result:
            return
        if n in temp:
            raise RuntimeError("Cycle detected")

        temp.add(n)
        for dependency in dependencies.get(n, []):
            visit(dependency, temp)
        result.append(n)

    result: list[str] = []

    unvisited = deque(wires)
    while unvisited:
        n = unvisited.popleft()
        temp: set[str] = set()
        visit(n, temp)

    return result


def part1(input: str) -> int:
    wires, dependencies = parse_input(input)
    sorted_wires = sort_wires(wires.keys(), dependencies)
    values: dict[str, int] = dict()

    for name in sorted_wires:
        values[name] = wires[name](values)

    result = values["a"]
    return result


def part2(input: str) -> int:
    wires, dependencies = parse_input(input)
    sorted_wires = sort_wires(wires.keys(), dependencies)
    values: dict[str, int] = dict()

    for name in sorted_wires:
        values[name] = wires[name](values)

    wires["b"] = make_value_operator(str(values["a"]))

    for name in sorted_wires:
        values[name] = wires[name](values)

    result = values["a"]
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day07_full.txt", part1, 16076),
        ("Part 2", "inputs/day07_full.txt", part2, 2797)
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
