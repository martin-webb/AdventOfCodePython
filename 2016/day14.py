from dataclasses import dataclass
from hashlib import md5
from pathlib import Path
import re
from time import time

YEAR = 2016
DAY = 14
NAME = "One-Time Pad"

TRIPLE_PATTERN = re.compile(r"(.)(\1){2}")


@dataclass
class CandidateKey:
    index: int
    pattern: str
    max_index: int


def solve(salt: str, key_count: int, stretches: int) -> int:
    candidates: list[CandidateKey] = []
    eligible_keys: list[int] = []

    done = False
    i = 0
    while True:
        h = md5(f"{salt}{i}".encode("utf-8"))
        digest = h.hexdigest()

        for _ in range(stretches):
            h = md5(digest.encode("utf-8"))
            digest = h.hexdigest()

        match = TRIPLE_PATTERN.search(digest)

        # Compare current digest against all candidates
        # XXX: Must do this in key ascending order, because earlier candidate
        # keys can be made eligible later (for example key 1 is made eligible
        # after the next 200 while key 2 is made available after the next 100),
        # in which case while key 2 was the first to be made eligible key 1 is
        # still considered as earlier, which affects us when we're looking for
        # the Nth key in order.
        # XXX: We mark deletions for a second pass instead of doing deletions
        # during the iteration, as these would need to either be done in
        # reverse order, flagged/tombstoned, or stored with a different
        # structure such as a heap, and we can get away without any of that for
        # this simple case by just doing deletions in a second pass.
        candidate_indices_to_delete: set[int] = set()

        for candidate in candidates:
            if candidate.pattern in digest and i <= candidate.max_index:
                eligible_keys.append(candidate.index)
                candidate_indices_to_delete.add(candidate.index)

            # Don't wait to check all the candidate keys once we hit the target
            if len(eligible_keys) == key_count:
                done = True
                break

        if done:
            break

        # Candidate key expiry (see above for reason we don't delete in-loop)
        for cidx in range(len(candidates)-1, -1, -1):
            candidate = candidates[cidx]
            if (i > candidate.max_index
                    or candidate.index in candidate_indices_to_delete):
                del candidates[cidx]

        # Is the current key a candidate?
        if match is not None:
            c = match.group(0)[0]

            candidate = CandidateKey(index=i, pattern=c*5, max_index=i+1000)
            candidates.append(candidate)

        i += 1

    result_index = eligible_keys[-1]
    return result_index


def part1(input: str) -> int:
    salt = input.strip()
    result = solve(salt, 64, 0)
    return result


def part2(input: str) -> int:
    salt = input.strip()
    result = solve(salt, 64, 2016)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day14_example.txt", part1, 22728),
        ("Part 1", "inputs/day14_full.txt", part1, 35186),
        ("Part 2", "inputs/day14_full.txt", part2, 22429),
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
