from pathlib import Path
from time import time

YEAR = 2015
DAY = 17
NAME = "No Such Thing as Too Much"


def container_combinations(n: int, C: list[int]) -> set[tuple[int, ...]]:
    def _combinations(n: int, result: tuple[int, ...], i: int = 0) -> None:
        if n > 0:
            for j in range(i, len(C)):
                if C[j] <= n:
                    _combinations(n - C[j], result + (j,), j+1)
                else:
                    _combinations(n, result, j+1)
        else:
            results.add(result)

    results: set[tuple[int, ...]] = set()
    _combinations(n, tuple())
    return results


def part1(input: str) -> int:
    containers = [int(n) for n in input.strip().split("\n")]
    sorted_containers = sorted(containers, reverse=True)
    C = container_combinations(150, sorted_containers)
    result = len(C)
    return result


def part2(input: str) -> int:
    containers = [int(n) for n in input.strip().split("\n")]
    sorted_containers = sorted(containers, reverse=True)
    C = container_combinations(150, sorted_containers)
    min_num_containers = len(sorted(C)[0])
    result = len([c for c in C if len(c) == min_num_containers])
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day17_full.txt", part1, 654),
        ("Part 2", "inputs/day17_full.txt", part2, 57)
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
