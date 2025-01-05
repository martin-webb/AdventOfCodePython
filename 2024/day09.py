from dataclasses import dataclass, field
import heapq
from time import time
from typing import Optional

YEAR = 2024
DAY = 9
NAME = "Disk Fragmenter"


@dataclass(order=True)
class FileBlock:
    position: int
    length: int
    id: int = field(compare=False)


@dataclass(order=True)
class FreeBlock:
    position: int
    length: int


def part1(input: str) -> int:
    input = input.strip()

    blocks: list[Optional[int]] = list()

    next_file_id = 0
    for i, x in enumerate(input):
        if i % 2 == 0:
            blocks += [next_file_id] * int(x)
            next_file_id += 1
        else:
            blocks += [None] * int(x)

    # Find the first free space
    next_free_index = 0
    while blocks[next_free_index] is not None:
        next_free_index += 1

    # Find the last block to move
    next_take_index = len(blocks) - 1
    while blocks[next_take_index] is None:
        next_take_index -= 1

    while next_free_index < next_take_index:
        blocks[next_free_index] = blocks[next_take_index]
        blocks[next_take_index] = None

        # Advance the pointer to the current free space
        next_free_index += 1
        while blocks[next_free_index] is not None:
            next_free_index += 1

        # Rewind the pointer to the current block to move
        next_take_index -= 1
        while blocks[next_take_index] is None:
            next_take_index -= 1

    checksum = 0
    for i, n in enumerate(blocks):
        if n is not None:
            checksum += i * n

    return checksum


def part2(input: str) -> int:
    input = input.strip()

    file_blocks: list[FileBlock] = list()
    free_blocks: list[FreeBlock] = list()

    position = 0
    next_file_id = 0
    for i, x in enumerate(input):
        if i % 2 == 0:
            file_blocks.append(
                FileBlock(position=position, length=int(x), id=next_file_id)
            )
            next_file_id += 1
        else:
            free_blocks.append(
                FreeBlock(position=position, length=int(x))
            )
        position += int(x)

    heapq.heapify(free_blocks)

    file_blocks = sorted(file_blocks, key=lambda b: b.id, reverse=True)
    for file_block in file_blocks:
        for free_block in free_blocks:
            if (free_block.length >= file_block.length
                    and free_block.position < file_block.position):

                # New free block with the position and length of the moved one
                new_free = FreeBlock(
                    position=file_block.position, length=file_block.length)

                # Update file block in place (position changes)
                file_block.position = free_block.position

                # Update free block in place (move forward and update length
                # to the remaining)
                free_block.position += file_block.length
                free_block.length = free_block.length - file_block.length

                # Add the new free block
                heapq.heappush(free_blocks, new_free)

                break

    # Final block list includes file blocks and free blocks ordered by position
    # NOTE: The free blocks include both ones that are still relevant to the
    # checksum (have a position before the last file block and a length > 0)
    # and ones that don't (have a position after the last file block and/or a
    # length of 0).
    # We don't explicitly filter out the free blocks that don't count towards
    # the checksum but the checksum calculation isn't affected by them, so we
    # can safely leave these in and don't need to handle heap removals above.
    final_blocks = sorted(file_blocks + free_blocks,  # type: ignore[operator]
                          key=lambda x: x.position)

    checksum = 0
    i = 0
    for block in final_blocks:
        if isinstance(block, FileBlock):
            j = i + block.length - 1
            mult = round(((i + j) / 2) * (j-i+1))  # Sum of i to j
            checksum += block.id * mult
        i += block.length

    return checksum


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day09_example.txt", part1, 1928),
        ("Part 1", "inputs/day09_full.txt", part1, 6398252054886),
        ("Part 2", "inputs/day09_example.txt", part2, 2858),
        ("Part 2", "inputs/day09_full.txt", part2, 6415666220005),
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
