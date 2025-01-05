from dataclasses import dataclass
from time import time
from typing import Any, Optional

DAY = 15
NAME = "Warehouse Woes"


@dataclass(eq=True, frozen=True)
class Vec2i:
    x: int
    y: int

    def __add__(self, other: Any) -> "Vec2i":
        if isinstance(other, tuple):
            return Vec2i(self.x + other[0], self.y + other[1])
        else:
            raise TypeError(
                "__add__() argument must be a tuple, " +
                f"not {other.__class__.__name__}"
            )


MOVES_TO_DIRECTIONS = {
    "^": Vec2i(0, -1),
    "v": Vec2i(0, 1),
    "<": Vec2i(-1, 0),
    ">": Vec2i(1, 0),
}


def try_push_one(
    W: dict[Vec2i, str],
    size: Vec2i,
    pos: Vec2i,
    direction: Vec2i
) -> bool:
    """
    Try to push a single space block in any direction, updating the warehouse
    map in-place and returning whether or not any blocks were moved.
    Recursively finds the next free space from the starting position in the
    given direction (if available) and works backwards, evaluating whether or
    not the push can be applied, applying the push if possible then returning
    whether or not the push was applied so the caller can know whether or not
    to apply their own move.
    Used for all movements in part 1 and for horizontal movements in part 2.
    """
    dst = Vec2i(pos.x + direction.x, pos.y + direction.y)
    if W[dst] == "#":
        return False

    elif W[dst] == ".":
        W[dst] = W[pos]
        W[pos] = "."
        return True

    else:
        if try_push_one(W, size, dst, direction):
            W[dst] = W[pos]
            return True
        else:
            return False


def _push_vert_wide(
    W: dict[Vec2i, str],
    size: Vec2i,
    pos_l: Vec2i,
    pos_r: Vec2i,
    direction: Vec2i,
    apply: bool
) -> bool:
    """
    Try to push a wide (two space) block in any direction, updating the
    warehouse map in-place and returning whether or not any blocks were moved.
    Recursively finds the next free space from the starting position in the
    given direction (if available) and works backwards, evaluating whether or
    not the push can be applied, applying the push if possible then returning
    whether or not the push was applied so the caller can know whether or not
    to apply their own move.
    Used for vertical movements in part 2, as for these you need to account
    for the case where one half of a block pushes the other half of another
    block, adding more vertical movement paths.
    For these cases, all implicated movement paths need to be evaluated to the
    end before actually applying the move, as pushing a wide block can affect
    multiple other blocks (not just in a straight line like in part 1), and all
    of these need to be movable for the push to work, so this flag allows to
    call this function once to validate the move and once more to apply it.
    The `apply` flag determines whether or not any block movement is actually
    applied.
    """
    assert direction == Vec2i(0, -1) or direction == Vec2i(0, 1)

    dst_l = Vec2i(pos_l.x + direction.x, pos_l.y + direction.y)
    dst_r = Vec2i(pos_r.x + direction.x, pos_r.y + direction.y)

    if W[dst_l] == "#" or W[dst_r] == "#":
        return False

    elif W[dst_l] == "." and W[dst_r] == ".":
        if apply:
            W[dst_l], W[pos_l] = W[pos_l], "."  # Left side
            W[dst_r], W[pos_r] = W[pos_r], "."  # Right side
        return True

    elif W[dst_l] == "]" and W[dst_r] == "[":
        pushed_left = _push_vert_wide(
            W, size, dst_l + (-1, 0), dst_l, direction, apply)
        pushed_right = _push_vert_wide(
            W, size, dst_r, dst_r + (1, 0), direction, apply)
        if pushed_left and pushed_right:
            if apply:
                W[dst_l], W[pos_l] = W[pos_l], "."  # Ahead
                W[dst_r], W[pos_r] = W[pos_r], "."  # One square left
            return True
        else:
            return False

    elif W[dst_l] == "[" and W[dst_r] == "]":
        if _push_vert_wide(W, size, dst_l, dst_r, direction, apply):
            if apply:
                W[dst_l], W[pos_l] = W[pos_l], "."  # Ahead
                W[dst_r], W[pos_r] = W[pos_r], "."  # One square left
            return True
        else:
            return False

    elif W[dst_l] == "]":
        # Pushing the right half of a box also pushes the left half
        if _push_vert_wide(W, size, dst_l + (-1, 0), dst_l, direction, apply):
            if apply:
                W[dst_l], W[pos_l] = W[pos_l], "."  # Ahead
                W[dst_r], W[pos_r] = W[pos_r], "."  # One square left
            return True
        else:
            return False

    elif W[dst_r] == "[":
        # Pushing the left half of a box also pushes the right half
        if _push_vert_wide(W, size, dst_r, dst_r + (1, 0), direction, apply):
            if apply:
                W[dst_l], W[pos_l] = W[pos_l], "."  # Ahead
                W[dst_r], W[pos_r] = W[pos_r], "."  # One square right
            return True
        else:
            return False

    assert False, "Should not get here"


def can_push_vert_wide(
    W: dict[Vec2i, str],
    size: Vec2i,
    pos_l: Vec2i,
    pos_r: Vec2i,
    direction: Vec2i
) -> bool:
    """
    Try to push a wide (two space) block in any direction, updating the
    warehouse map in-place and returning whether or not any blocks were moved.
    applyesn't apply the move, only testing whether or not it can be applyne.
    """
    return _push_vert_wide(W, size, pos_l, pos_r, direction, False)


def push_vert_wide(
    W: dict[Vec2i, str],
    size: Vec2i,
    pos_l: Vec2i,
    pos_r: Vec2i,
    direction: Vec2i
) -> bool:
    """
    Try to push a wide (two space) block in any direction, updating the
    warehouse map in-place and returning whether or not any blocks were moved.
    Applies the move.
    """
    return _push_vert_wide(W, size, pos_l, pos_r, direction, True)


def push_part1(
    W: dict[Vec2i, str],
    size: Vec2i,
    pos: Vec2i,
    move: str
) -> Vec2i:
    """
    Simulates a single push for part 1, updating the warehouse data in place
    and returning the updated robot position (the updated position can be the
    same if the robot did not move).
    """
    direction = MOVES_TO_DIRECTIONS[move]
    dst = Vec2i(pos.x + direction.x, pos.y + direction.y)
    if W[dst] == ".":
        return dst

    elif W[dst] == "#":
        return pos

    elif W[dst] == "O":
        if try_push_one(W, size, dst, direction):
            return dst
        else:
            return pos

    assert False, "Should not get here"


def push_part2(
    W: dict[Vec2i, str],
    size: Vec2i,
    pos: Vec2i,
    move: str
) -> Vec2i:
    """
    Simulates a single push for part 2, updating the warehouse data in place
    and returning the updated robot position (the updated position can be the
    same if the robot did not move).
    The difference for the part 2 version of this is that for vertical
    movements you need to evaluate all implicated paths ahead of moving to know
    if you can actually apply the move.
    For all part 1 moves and part 2 horizontal moves you can evaluate and move
    at the same time, as each movement has only one direct dependency and these
    can be evaluated from the end, but part 2 vertical movements have to be
    checked first.
    """
    direction = MOVES_TO_DIRECTIONS[move]
    dst = Vec2i(pos.x + direction.x, pos.y + direction.y)
    if W[dst] == ".":
        return dst

    elif W[dst] == "#":
        return pos

    elif W[dst] == "[" or W[dst] == "]":
        is_horizontal_move = direction.x != 0
        is_vertical_move = direction.y != 0
        assert is_horizontal_move ^ is_vertical_move

        if is_horizontal_move:
            if try_push_one(W, size, dst, direction):
                return dst
            else:
                return pos

        elif is_vertical_move:
            if W[dst] == "[":
                if can_push_vert_wide(W, size, dst, dst+(1, 0), direction):
                    push_vert_wide(W, size, dst, dst+(1, 0), direction)
                    return dst
                else:
                    return pos

            elif W[dst] == "]":
                if can_push_vert_wide(W, size, dst+(-1, 0), dst, direction):
                    push_vert_wide(W, size, dst+(-1, 0), dst, direction)
                    return dst
                else:
                    return pos

    assert False, "Should not get here"


def part1(input: str) -> int:
    warehouse_desc, moves_desc = input.strip().split("\n\n")

    W: dict[Vec2i, str] = dict()
    robot: Optional[Vec2i] = None

    for y, line in enumerate(warehouse_desc.split("\n")):
        for x, m in enumerate(line):
            W[Vec2i(x, y)] = m
            if m == "@":
                robot = Vec2i(x, y)

    assert robot is not None

    size = Vec2i(x + 1, y + 1)

    for line in moves_desc.split("\n"):
        for move in line:
            moved_to = push_part1(W, size, robot, move)
            # Update in this order so we can update in place without deleting
            # the robot from the map...
            W[robot] = "."
            W[moved_to] = "@"
            robot = moved_to

    gps_sum = 0
    for y in range(size.y):
        for x in range(size.x):
            if W[Vec2i(x, y)] == "O":
                gps_sum += 100 * y + x

    return gps_sum


def part2(input: str) -> int:
    warehouse_desc, moves_desc = input.strip().split("\n\n")

    W: dict[Vec2i, str] = dict()
    robot: Optional[Vec2i] = None

    for y, line in enumerate(warehouse_desc.split("\n")):
        for x, m in enumerate(line):
            if m == "#":
                W[Vec2i(x * 2, y)] = "#"
                W[Vec2i(x * 2 + 1, y)] = "#"
            elif m == "O":
                W[Vec2i(x * 2, y)] = "["
                W[Vec2i(x * 2 + 1, y)] = "]"
            elif m == ".":
                W[Vec2i(x * 2, y)] = "."
                W[Vec2i(x * 2 + 1, y)] = "."
            elif m == "@":
                W[Vec2i(x * 2, y)] = "@"
                W[Vec2i(x * 2 + 1, y)] = "."
                robot = Vec2i(x * 2, y)

    assert robot is not None

    size = Vec2i((x + 1) * 2, (y + 1))

    for line in moves_desc.split("\n"):
        for move in line:
            moved_to = push_part2(W, size, robot, move)
            # Update in this order so we can update in place without deleting
            # the robot from the map...
            W[robot] = "."
            W[moved_to] = "@"
            robot = moved_to

    gps_sum = 0
    for y in range(size.y):
        for x in range(size.x):
            if W[Vec2i(x, y)] == "[":
                gps_sum += 100 * y + x

    return gps_sum


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day15_example_small.txt", part1, 2028),
        ("Part 1", "inputs/day15_example_large.txt", part1, 10092),
        ("Part 1", "inputs/day15_full.txt", part1, 1456590),
        ("Part 2", "inputs/day15_example_large.txt", part2, 9021),
        ("Part 2", "inputs/day15_full.txt", part2, 1489116),
    ):
        with open(filename) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
