from collections import Counter
from pathlib import Path
from time import time

YEAR = 2023
DAY = 7
NAME = "Camel Cards"


def hand_type(hand: str) -> int:
    """
    >>> hand_type("AAAAA")
    1
    >>> hand_type("AA8AA")
    2
    >>> hand_type("23332")
    3
    >>> hand_type("TTT98")
    4
    >>> hand_type("23432")
    5
    >>> hand_type("A23A4")
    6
    >>> hand_type("23456")
    7
    """
    counts = Counter(hand)
    distribution = sorted(counts.values())

    # Five of a kind
    if distribution == [5]:
        return 1

    # Four of a kind
    if distribution == [1, 4]:
        return 2

    # Full house
    if distribution == [2, 3]:
        return 3

    # Three of a kind
    if distribution == [1, 1, 3]:
        return 4

    # Two pair
    if distribution == [1, 2, 2]:
        return 5

    # One pair
    if distribution == [1, 1, 1, 2]:
        return 6

    # High card
    if distribution == [1, 1, 1, 1, 1]:
        return 7

    raise RuntimeError(f"Can't rank hand '{hand}'")


def hand_value(hand: str) -> int:
    """
    >>> hand_value("2AAAA")
    355540
    >>> hand_value("33332")
    333320
    >>> hand_value("77788")
    777880
    >>> hand_value("77888")
    778880
    """
    vals = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    # Any earlier higher-ranking card in a hand will always mean that that hand
    # outranks the one it is being compared to, so we need to increase the
    # value of earlier cards enough to ensure that even if all subsequent cards
    # are of the highest possible value the hand with the earlier card with the
    # high rank will stay higher ranked.
    # We use pow(100) to increase the value of earlier cards by a value large
    # enough to guarantee this (our highest value is 14 (A), so pow(10) isn't
    # enough).
    # NOTE: This is a bit of a side effect of writing a custom hand sort
    # function that is intended to return a sortable value for a single hand
    # instead of a comparison function that takes two hands where we could
    # always exit early (return -1, 0 or 1) for any higher ranking card.
    # This is a case where the opposite of functools.cmp_to_key feels like it
    # would be useful.
    value = sum(
        [(int(pow(100, (5-i))) * vals[x]) for i, x in enumerate(hand)]
    )
    return value


def hand_value_joker(hand: str) -> int:
    """
    >>> hand_value("JJJJJ")
    10101010100
    >>> hand_value("AAAAA")
    141414141400
    >>> hand_value("AJJJJ")
    140101010100
    """
    vals = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
        "J": 1,
    }
    # Any earlier higher-ranking card in a hand will always mean that that hand
    # outranks the one it is being compared to, so we need to increase the
    # value of earlier cards enough to ensure that even if all subsequent cards
    # are of the highest possible value the hand with the earlier card with the
    # high rank will stay higher ranked.
    # We use pow(100) to increase the value of earlier cards by a value large
    # enough to guarantee this (our highest value is 14 (A), so pow(10) isn't
    # enough).
    # NOTE: This is a bit of a side effect of writing a custom hand sort
    # function that is intended to return a sortable value for a single hand
    # instead of a comparison function that takes two hands where we could
    # always exit early (return -1, 0 or 1) for any higher ranking card.
    # This is a case where the opposite of functools.cmp_to_key feels like it
    # would be useful.
    value = sum(
        [(int(pow(100, (5-i))) * vals[x]) for i, x in enumerate(hand)]
    )
    return value


def hand_type_joker(hand: str) -> int:
    counts = Counter(hand)

    hand_type_original = hand_type(hand)
    if "J" in hand and hand != "JJJJJ":
        most_common_letter = counts.most_common()[0][0]
        if most_common_letter == "J":
            most_common_letter = counts.most_common()[1][0]
        hand_jokerised = hand.replace("J", most_common_letter)
        hand_type_jokerised = hand_type(hand_jokerised)
        if hand_type_jokerised < hand_type_original:
            return hand_type_jokerised
        else:
            return hand_type_original
    else:
        return hand_type_original


def part1(input: str) -> int:
    winnings = 0

    entries = []
    for line in input.strip().split("\n"):
        hand, bid_str = line.split()
        entries.append((hand, int(bid_str)))

    sorted_entries = sorted(
        entries, key=lambda x: (hand_type(x[0]), -hand_value(x[0]))
    )

    for i, entry in enumerate(sorted_entries):
        mult = len(sorted_entries) - i
        winnings += entry[1] * mult

    return winnings


def part2(input: str) -> int:
    winnings = 0

    entries = []
    for line in input.strip().split("\n"):
        hand, bid_str = line.split()
        entries.append((hand, int(bid_str)))

    sorted_entries = sorted(
        entries, key=lambda x: (hand_type_joker(x[0]), -hand_value_joker(x[0]))
    )

    for i, entry in enumerate(sorted_entries):
        mult = len(sorted_entries) - i
        winnings += entry[1] * mult

    return winnings


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day07_example.txt", part1, 6440),
        ("Part 1", "inputs/day07_full.txt", part1, 255048101),
        ("Part 2", "inputs/day07_example.txt", part2, 5905),
        ("Part 2", "inputs/day07_full.txt", part2, 253718286),
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
