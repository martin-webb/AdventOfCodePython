from collections.abc import Callable
from functools import partial
from itertools import permutations
from pathlib import Path
from time import time

YEAR = 2016
DAY = 21
NAME = "Scrambled Letters and Hash"

ScrambleFunc = Callable[[list[str]], list[str]]


def make_swap_position(a: int, b: int) -> ScrambleFunc:
    def do(val: list[str]) -> list[str]:
        val[a], val[b] = val[b], val[a]
        return val
    return do


def make_swap_letter(a: str, b: str) -> ScrambleFunc:
    def do(val: list[str]) -> list[str]:
        val = [a if s == b else b if s == a else s
               for s in val]
        return val
    return do


def make_reverse(a: int, b: int) -> ScrambleFunc:
    def do(val: list[str]) -> list[str]:
        val = val[:a] + val[a:b+1][::-1] + val[b+1:]
        return val
    return do


def make_move(a: int, b: int) -> ScrambleFunc:
    def do(val: list[str]) -> list[str]:
        val.insert(b, val.pop(a))
        return val
    return do


def make_rotate_left(a: int) -> ScrambleFunc:
    def do(val: list[str]) -> list[str]:
        for _ in range(a):
            val = val[1:] + val[0:1]
        return val
    return do


def make_rotate_right(a: int) -> ScrambleFunc:
    def do(val: list[str]) -> list[str]:
        for _ in range(a):
            val = val[-1:] + val[:-1]
        return val
    return do


def make_rotate_position(a: str) -> ScrambleFunc:
    def do(val: list[str]) -> list[str]:
        idx = val.index(a)
        num_rotations = 1 + idx
        if idx >= 4:
            num_rotations += 1
        for _ in range(num_rotations):
            val = val[-1:] + val[:-1]
        return val
    return do


def parse_input(input: str) -> list[ScrambleFunc]:
    """
    Unnecessary closure-based solution.
    """
    operations: list[ScrambleFunc] = list()

    for line in input.strip().split("\n"):
        parts = line.split()

        if parts[0] == "swap" and parts[1] == "position":
            operation = make_swap_position(int(parts[2]), int(parts[5]))

        elif parts[0] == "swap" and parts[1] == "letter":
            operation = make_swap_letter(parts[2], parts[5])

        elif parts[0] == "reverse":
            operation = make_reverse(int(parts[2]), int(parts[4]))

        elif parts[0] == "move":
            operation = make_move(int(parts[2]), int(parts[5]))

        elif parts[0] == "rotate" and parts[1] == "left":
            operation = make_rotate_left(int(parts[2]))

        elif parts[0] == "rotate" and parts[1] == "right":
            operation = make_rotate_right(int(parts[2]))

        elif parts[0] == "rotate" and parts[1] == "based":
            operation = make_rotate_position(parts[6])

        else:
            raise RuntimeError(f"Unsupported operation: '{line}'")

        operations.append(operation)

    return operations


def scramble(password: tuple[str, ...], operations: list[ScrambleFunc]) -> str:
    intermediate = list(password)

    for operation in operations:
        intermediate = operation(intermediate)

    scrambled = "".join(intermediate)
    return scrambled


def part1(input: str, password: str) -> str:
    operations = parse_input(input)
    result = scramble(tuple(password), operations)
    return result


def part2(input: str, scrambled: str) -> str:
    """
    Brute force test the scrambled version of every possible input instead of
    reversing the scrambling function (as a first attempt, I want to revisit
    this).
    """
    operations = parse_input(input)

    for candidate in permutations(scrambled, len(scrambled)):
        scrambled_candidate = scramble(candidate, operations)
        if scrambled_candidate == scrambled:
            result = "".join(candidate)
            break

    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day21_example.txt",
         partial(part1, password="abcde"), "decab"),
        ("Part 1", "inputs/day21_full.txt",
         partial(part1, password="abcdefgh"), "aefgbcdh"),
        ("Part 2", "inputs/day21_full.txt",
         partial(part2, scrambled="fbgdceah"), "egcdahbf"),
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
