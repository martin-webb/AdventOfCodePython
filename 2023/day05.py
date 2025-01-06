from collections import deque
from dataclasses import dataclass
from pathlib import Path
import sys
from time import time

YEAR = 2023
DAY = 5
NAME = "If You Give A Seed A Fertilizer"


@dataclass
class Mapping:
    src: int
    dst: int
    range: int

    @property
    def src_end(self) -> int:
        """
        Source range end (inclusive).
        """
        return self.src + self.range - 1

    @property
    def dst_end(self) -> int:
        """
        Destination range end (inclusive).
        """
        return self.dst + self.range - 1


def seed_ranges_to_location(
        ranges: list[tuple[int, int]],
        maps: list[list[Mapping]],
        i: int = 0) -> int:
    if i < len(maps):
        candidates = []
        ranges_queue = deque(ranges)
        while ranges_queue:
            r = ranges_queue.popleft()
            for m in maps[i]:
                offset = m.dst - m.src

                # Case 1 - seed range fully enclosed in mapping
                # 1 range -> 1 range (1 mapped)
                if r[0] >= m.src and r[1] <= m.src_end:
                    candidates.append((r[0] + offset, r[1] + offset))
                    break

                # Case 2 - seed range overlaps mapping to the left
                # 1 range -> 2 ranges (1 mapped, 1 new candidate)
                elif r[0] < m.src and r[1] >= m.src and r[1] <= m.src_end:
                    candidates.append((m.dst, r[1] + offset))
                    ranges_queue.append((r[0], m.src - 1))
                    break

                # Case 3 - seed range overlaps mapping to the right
                # 1 range -> 2 ranges (1 mapped, 1 new candidate)
                elif r[0] >= m.src and r[0] <= m.src_end and r[1] > m.src_end:
                    candidates.append((r[0] + offset, m.dst_end))
                    ranges_queue.append((m.src_end + 1, r[1]))
                    break

                # Case 4 - seed range fully outside mapping
                # 1 range -> 3 ranges (1 mapped, 2 new candidates)
                # NOTE: The new candidate ranges can be different based on
                # the order that mapping ranges are checked but will eventually
                # map to a consistent set of candidate ranges for the next set
                # of mappings
                elif r[0] < m.src and r[1] > m.src_end:
                    candidates.append((m.dst, m.dst_end))
                    ranges_queue.append((r[0], m.src - 1))
                    ranges_queue.append((m.src_end + 1, r[1]))
                    break
            else:
                candidates.append(r)
        return seed_ranges_to_location(candidates, maps, i + 1)
    else:
        return min([r[0] for r in ranges])


def part1(input: str) -> int:
    seeds: list[int] = []
    maps: list[list[Mapping]] = []

    for line in input.strip().split("\n\n"):
        if line.startswith("seeds"):
            seeds_str = line.split(": ")[1]
            seeds = [int(s) for s in seeds_str.split()]
        elif "map" in line:
            maps.append([])
            for description in line.split("\n")[1:]:
                values = [int(s) for s in description.split()]
                m = Mapping(src=values[1], dst=values[0], range=values[2])
                maps[-1].append(m)

    min_location = sys.maxsize
    for seed in seeds:
        location = seed_ranges_to_location([(seed, seed)], maps)
        min_location = min(min_location, location)

    return min_location


def part2(input: str) -> int:
    seed_ranges: list[tuple[int, int]] = []
    maps: list[list[Mapping]] = []

    for line in input.strip().split("\n\n"):
        if line.startswith("seeds"):
            _, seed_nums_s = line.split(":")
            seed_nums = [int(s.strip()) for s in seed_nums_s.split()]
            seed_pairs = zip(seed_nums[::2], seed_nums[1::2])
            for start, range_ in seed_pairs:
                seed_range = (start, start + range_ - 1)
                seed_ranges.append(seed_range)
        elif "map" in line:
            maps.append([])
            for description in line.split("\n")[1:]:
                values = [int(s) for s in description.split()]
                r = Mapping(src=values[1], dst=values[0], range=values[2])
                maps[-1].append(r)

    min_location = sys.maxsize
    for seed_range in seed_ranges:
        location = seed_ranges_to_location([seed_range], maps)
        min_location = min(min_location, location)

    return min_location


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day05_example.txt", part1, 35),
        ("Part 1", "inputs/day05_full.txt", part1, 525792406),
        ("Part 2", "inputs/day05_example.txt", part2, 46),
        ("Part 2", "inputs/day05_full.txt", part2, 79004094),
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
