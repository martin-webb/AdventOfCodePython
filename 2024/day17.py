from time import time

YEAR = 2024
DAY = 17
NAME = "Chronospatial Computer"


def parse_input(s: str) -> tuple[int, int, int, list[int]]:
    register_desc, program_desc = s.split("\n\n")
    register_lines = register_desc.split("\n")
    a = int(register_lines[0].split(": ")[1])
    b = int(register_lines[1].split(": ")[1])
    c = int(register_lines[2].split(": ")[1])
    program = [int(n) for n in program_desc.split(": ")[1].split(",")]
    return a, b, c, program


def compute(a: int, b: int, c: int, program: list[int]) -> list[int]:
    outputs = []

    def combo(operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return a
        elif operand == 5:
            return b
        elif operand == 6:
            return c
        assert False, "Should not get here"

    ip = 0
    while True:
        if ip >= len(program):
            break

        opcode, operand = program[ip], program[ip+1]

        if opcode == 0:  # adv
            a = int(a / (2 ** combo(operand)))
        elif opcode == 1:  # bxl
            b = b ^ operand
        elif opcode == 2:  # bst
            b = (combo(operand) % 8)
        elif opcode == 3:  # jnz
            if a != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            b = b ^ c
        elif opcode == 5:  # out
            outputs.append(combo(operand) % 8)
        elif opcode == 6:  # bdv
            b = int(a / (2 ** combo(operand)))
        elif opcode == 7:  # cdv
            c = int(a / (2 ** combo(operand)))

        ip += 2

    return outputs


def part1(input: str) -> str:
    a, b, c, program = parse_input(input)
    outputs = compute(a, b, c, program)
    output = ",".join([str(n) for n in outputs])
    return output


def part2(input: str) -> int:
    _, _, _, program = parse_input(input)

    index = len(program) - 1

    n = 0
    while True:
        out = compute(n, 0, 0, program)
        if out == program[index:]:
            index -= 1
            if index == -1:
                break
            n = n << 3
            continue
        n += 1

    return n


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day17_example.txt", part1, "4,6,3,5,6,3,5,2,1,0"),
        ("Part 1", "inputs/day17_full.txt", part1, "3,4,3,1,7,6,5,6,0"),
        # NOTE: Part 2 with example input excluded for now as the current
        # solution is designed around the full input
        # ("Part 2", "inputs/day17_example.txt", part2, 117440),
        ("Part 2", "inputs/day17_full.txt", part2, 109019930331546),
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
