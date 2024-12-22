"""Day 17"""
T_Registers = tuple[int, int, int]
T_Program = list[int]
T_Data = tuple[T_Registers, T_Program]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        raw_registers, raw_program = fin.read().strip().split("\n\n")

        registers = tuple(
            int(line.split(": ")[1])
            for line in raw_registers.split("\n")
        )
        instructions = [int(i) for i in raw_program.split(": ")[1].split(",")]
        return registers, instructions


def run_program(registers: T_Registers, instructions: T_Program) -> list[int]:
    ip = 0

    A, B, C = registers

    def _combo(value: int) -> int:
        if 0 <= value <= 3:
            return value

        if value == 4:
            return A

        if value == 5:
            return B

        if value == 6:
            return C

    out = []
    # print(f"Initial: ({A=}, {B=}, {C=}")
    # print("-----")
    while ip < len(instructions):
        opcode, operand = instructions[ip], instructions[ip + 1]

        if opcode == 0:  # adv
            # print(f"adv: A = {A} / 2**{_combo(operand)}")
            A = int(A / 2**_combo(operand))
        elif opcode == 1:  # bxl
            # print(f"bxl: B = {B} ^ {operand}")
            B = B ^ operand
        elif opcode == 2:  # bst
            # print(f"bst: B = {_combo(operand)} % 8")
            B = _combo(operand) % 8
        elif opcode == 3:  # jnz
            # if A == 0:
            #     print("jnz: noop")
            if A != 0:
                # print(f"jnz: IP = {operand}")
                ip = operand
                ip -= 2  # To mitigate the later addition of 2
        elif opcode == 4:  # bxc
            # print(f"bxc: B = {B} ^ {C}")
            B = B ^ C
        elif opcode == 5:  # out
            # print(f"out: {_combo(operand)} % 8")
            out.append(_combo(operand) % 8)
        elif opcode == 6:  # bdv
            # print(f"bdv: B = {A} / 2**{_combo(operand)}")
            B = int(A / 2**_combo(operand))
        elif opcode == 7:  # cdv
            # print(f"cdv: C = {A} / 2**{_combo(operand)}")
            C = int(A / 2**_combo(operand))

        ip += 2
        # print(f"State: ({A=}, {B=}, {C=}), {out=}")
        # print("-----")

    return out #",".join([str(o) for o in out])



def solve_part_two(instructions: T_Program) -> int:
    """
    2,4,1,5,7,5,1,6,0,3,4,6,5,5,3,0

    2,4 --> bst: B = A % 8
    1,5 --> bxl: B = B ^ 5
    7,5 --> cdv: C = A / 2**B
    1,6 --> bxl: B = B ^ 6
    0,3 --> adv: A = A / 2**3
    4,6 --> bxc: B = B ^ C
    5,5 --> out: B % 8
    3,0 --> jnz: IP = 0
    """
    A_values = []

    n = len(instructions)
    all_candidates = [[0] * n]

    for idx in range(n):
        new_candidates = []

        for candidate in all_candidates:
            for d in range(8):
                candidate[idx] = d
                A = int(''.join(str(c) for c in candidate), base=8)
                out = run_program((A, 0, 0), instructions)

                if out == instructions:
                    A_values.append(A)

                elif list(reversed(out))[:(idx + 1)] == list(reversed(instructions))[:(idx + 1)]:
                    new_candidates.append(candidate.copy())

        all_candidates = new_candidates

    return min(A_values)


def run_tests() -> None:
    registers, instructions = read_input("data/example.txt")
    assert run_program(registers, instructions) == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]

    # --- Example (second part) ---
    # This program divides A by 8, then outputs the last three digits and repeats,
    # 117_440 is 011_100_101_011_000_000 in binary (looking at the 3-bit blocks
    # we can see that they are the same as in the program, except for the last
    # 0 operand, but this is handled in the program)
    assert run_program((117_440, 0, 0), [0, 3, 5, 4, 3, 0]) == [0, 3, 5, 4, 3, 0]


def main() -> None:
    # run_tests()

    registers, instructions = read_input("data/input.txt")

    solution_one = run_program(registers, instructions)
    print("Part one:", solution_one)

    solution_two = solve_part_two(instructions)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

