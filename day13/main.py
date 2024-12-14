"""Day 13"""
import re
import sys
from itertools import product


T_Position = tuple[int, int]
T_MachineConfig = tuple[T_Position, T_Position, T_Position]
T_Data = list[T_MachineConfig]


def read_input(file: str) -> T_Data:
    data = []
    with open(file, "r") as fin:
        for raw_machine_cfg in fin.read().strip().split("\n\n"):
            btn_regex = re.compile("Button (?:A|B): X\+(\d+), Y\+(\d+)")
            prize_regex = re.compile("Prize: X=(\d+), Y=(\d+)")

            parts = raw_machine_cfg.split("\n")
            button_A = tuple(
                int(v)
                for v in re.match(btn_regex, parts[0]).groups()
            )
            button_B = tuple(
                int(v)
                for v in re.match(btn_regex, parts[1]).groups()
            )
            prize = tuple(
                int(v)
                for v in re.match(prize_regex, parts[2]).groups()
            )
            data.append((button_A, button_B, prize))
    return data


def solve_naive(
    Ax: int,
    Ay: int,
    Bx: int,
    By: int,
    Px: int,
    Py: int,
    max_iter: int = 100,
) -> int | None:
    # Naive approach - just test all the cases and find the minimum
    num_tokens = sys.maxsize
    for A, B in product(range(1, max_iter + 1), repeat=2):
        pos = A * Ax + B * Bx, A * Ay + B * By

        if pos == (Px, Py):
            tokens = 3 * A + B
            num_tokens = min(num_tokens, tokens)

    if num_tokens != sys.maxsize:
        return num_tokens

    return None


def solve_efficient(
    Ax: int,
    Ay: int,
    Bx: int,
    By: int,
    Px: int,
    Py: int,
) -> int | None:
    """
    [[Ax Bx],    [A     [Px
     [Ay By]]  *  B]  =  Py]


    inv([[Ax Bx],            [[By -Bx],
         [Ay By]]) = 1/det *  [-Ay Ax]]


    [A          [Px
     B] = inv *  Py]

    ----
    A = 1/det * (By * Px + (-Bx) * Py)
    B = 1/det * ((-Ay) * Px + Ax * Py)
    """
    det = Ax * By - Bx * Ay
    if det == 0:
        return None

    A_num = By * Px + (-Bx) * Py
    B_num = (-Ay) * Px + Ax * Py

    if B_num % det == 0 and A_num % det == 0:
        A = A_num // det
        B = B_num // det
        num_tokens = 3 * A + B

        return num_tokens

    return None


def solve_part_one(data: T_Data, fn) -> int:
    result = 0
    
    for (Ax, Ay), (Bx, By), (Px, Py) in data:
        num_tokens = fn(Ax, Ay, Bx, By, Px, Py)
        if num_tokens:
            result += num_tokens

    return result


def solve_part_two(data: T_Data) -> int:
    result = 0

    offset = 10_000_000_000_000

    for (Ax, Ay), (Bx, By), (Px, Py) in data:
        num_tokens = solve_efficient(
            Ax=Ax,
            Ay=Ay,
            Bx=Bx,
            By=By,
            Px=Px + offset,
            Py=Py + offset,
        )
        if num_tokens:
            result += int(num_tokens)
        
    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data, solve_naive) == 480
    assert solve_part_one(data, solve_efficient) == 480


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data, solve_efficient)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

