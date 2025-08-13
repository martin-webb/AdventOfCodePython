from pathlib import Path
from time import time

YEAR = 2016
DAY = 19
NAME = "An Elephant Named Joseph"


def part1(input: str) -> int:
    """
    Iterative solution (over closed-form or recursive solution for the Josephus
    problem) as a first pass (famous last words).
    One insight useful for this is that we don't actually need to track the
    number of presents, only the positions of relevant elf numbers. It's also
    not even part of the question and the total number is just the number of
    elves as they all contribute one present.
    However, if we _did_ want to track the present count with this approach
    then we can simply keep track of two counts, a 'first' and 'last' count.
    Then, for each iteration, update the counts as follows:
    For an even number of elves in play, the first of each pair (including the
    last, as they'll become the first of each pair) gets all the presents from
    the other. We don't actually need to track the number as it just doubles
    for every iteration, or we can set the present count based on the number of
    iterations at that step.
    presents_first *= 2
    presents_last *= 2
    For an odd number of elves in play, we essentially have an extra elf that
    doesn't get double presents but instead gets the number of presents that
    the first has (after the first has taken their extra ones).
    presents_first *= 2
    presents_last += presents_first
    But we don't need any of this.
    """
    num_elves = int(input.strip())

    first_pos = 1
    last_pos = num_elves

    iters = 1
    while num_elves > 1:
        if num_elves % 2 == 0:
            # As the second in each pair takes all presents taken away the last
            # elf in play jumps back by a number that doubles each time (or we
            # can track the number of iterations).
            last_pos -= 2 ** (iters-1)
        else:
            # As the extra elf takes from the first our new first elf moves
            # forward
            first_pos += 2 ** iters
            # And we lose the first elf as they have no presents left
            num_elves -= 1
        num_elves = (num_elves // 2) + (num_elves % 2)
        iters += 1

    return first_pos


def part2(input: str) -> int:
    """
    Iterative solution as a first pass (famous last words).
    """
    num_elves = int(input.strip())

    elves = list(range(1, num_elves+1))

    i = 0
    while len(elves) > 1:
        j = (i + (len(elves) // 2)) % len(elves)
        del elves[j]
        if i < j:
            i = (i + 1) % len(elves)
        elif i == len(elves):
            i = 0

    return elves[0]


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day19_example.txt", part1, 3),
        ("Part 1", "inputs/day19_full.txt", part1, 1808357),
        ("Part 2", "inputs/day19_example.txt", part2, 2),
        ("Part 2", "inputs/day19_full.txt", part2, 1407007)
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
