from dataclasses import dataclass
from pathlib import Path
from time import time

YEAR = 2025
DAY = 5
NAME = "Cafeteria"


@dataclass(frozen=True, order=True)
class Range:
    """
    Inclusive range.
    """
    src: int
    dst: int

    @property
    def len(self) -> int:
        return self.dst - self.src + 1


def parse_input(input: str) -> tuple[list[Range], list[int]]:
    ingredient_ranges: list[Range] = list()
    available_ids: list[int] = list()

    lines_top, lines_bottom = input.strip().split("\n\n")

    for line in lines_top.split("\n"):
        src, dst = [int(c) for c in line.split("-")]
        ingredient_ranges.append(Range(src, dst))

    for line in lines_bottom.split("\n"):
        available_ids.append(int(line))

    return ingredient_ranges, available_ids


def split_ranges(R: list[Range]) -> list[Range]:
    """
    Recursive range splitter.
    """
    R = sorted(R)

    for i in range(len(R)-1):
        j = i + 1
        a, b = R[i], R[j]

        assert a.src <= a.dst
        assert b.src <= b.dst
        assert not b.src < a.src, f"b.src < a.src for {a=}, {b=}"

        if a.src == b.src:  # Aligned on left edge
            if b.dst < a.dst:  # Splits
                return split_ranges(
                    R[:i] + [
                        Range(b.src, b.dst),
                        Range(b.dst+1, a.dst)
                    ] + R[j+1:]
                )

            elif b.dst > a.dst:  # Extends
                return split_ranges(
                    R[:i] + [
                        Range(b.src, a.dst),
                        Range(a.dst+1, b.dst)
                    ] + R[j+1:]
                )

            elif a.dst == b.dst:  # Overlaps
                return split_ranges(
                    R[:i] + [
                        Range(b.src, b.dst)
                    ] + R[j+1:]
                )

            else:
                assert False, \
                    f"Aligned on left edge, split not handled for: {a=},{b=}"

        elif a.src < b.src < a.dst:  # Inset from left edge
            if b.dst < a.dst:  # Splits
                return split_ranges(
                    R[:i] + [
                        Range(a.src, b.src-1),
                        Range(b.src, b.dst),
                        Range(b.dst+1, a.dst)
                    ] + R[j+1:]
                )

            elif b.dst > a.dst:  # Extends
                return split_ranges(
                    R[:i] + [
                        Range(a.src, b.src-1),
                        Range(b.src, a.dst),
                        Range(a.dst+1, b.dst)
                    ] + R[j+1:]
                )

            elif b.dst == a.dst:  # Overlaps
                return split_ranges(
                    R[:i] + [
                        Range(a.src, b.src-1),
                        Range(b.src, a.dst)
                    ] + R[j+1:]
                )

            else:
                assert False, \
                    f"Inset on left edge, split not handled for: {a=},{b=}"

        elif a.dst == b.src:  # Alignment of src and dst
            # XXX: Move a's dst by 1 instead of b's src
            return split_ranges(
                R[:i] + [
                    Range(a.src, a.dst-1),
                    Range(b.src, b.dst)
                ] + R[j+1:]
            )

        elif a.dst < b.src:
            pass

        else:
            assert False, \
                f"split not handled for: {a=},{b=}"

    return R


def part1(input: str) -> int:
    ingredient_ranges, available_ids = parse_input(input)

    num_fresh = 0
    for n in available_ids:
        for r in ingredient_ranges:
            if n >= r.src and n <= r.dst:
                num_fresh += 1
                break

    return num_fresh


def part2(input: str) -> int:
    ingredient_ranges, _ = parse_input(input)
    split = split_ranges(ingredient_ranges)
    total = sum(r.len for r in split)
    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day05_example.txt", part1, 3),
        ("Part 1", "inputs/day05_full.txt", part1, 865),
        ("Part 2", "inputs/day05_example.txt", part2, 14),
        ("Part 2", "inputs/day05_full.txt", part2, 352556672963116),
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
            assert result == expected, f"difference: {abs(result-expected)}"


if __name__ == "__main__":
    main()
