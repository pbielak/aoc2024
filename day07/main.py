"""Day 07"""
from itertools import product

T_Data = list[tuple[int, list[int]]]


def read_input(file: str) -> T_Data:
    equations = []
    with open(file, "r") as fin:
        for line in fin:
            expected_result, raw_numbers = line.strip().split(":")
            numbers = [int(num) for num in raw_numbers.strip().split(" ")]
            equations.append((int(expected_result), numbers))

    return equations


def eval_equation(numbers: list[int], ops: list) -> int:
    result = numbers.copy()

    for op in ops:
        x, y = result[0], result[1]
        result = [op(x, y), *result[2:]]

    assert len(result) == 1
    return result[0]


def can_be_solved(
    expected_result: int,
    numbers: list[int],
    operators: list,
) -> bool:
    for ops in product(
        operators,
        repeat=len(numbers) - 1,
    ):
        eq_result = eval_equation(numbers, ops)
        if eq_result == expected_result:
            return True

    return False


def solve_part_one(data: T_Data) -> int:
    result = 0

    for expected_result, numbers in data:
        if can_be_solved(
            expected_result=expected_result,
            numbers=numbers,
            operators=[
                lambda x, y: x * y,
                lambda x, y: x + y
            ],
        ):
            result += expected_result

    return result


def solve_part_two(data: T_Data) -> int:
    result = 0

    for expected_result, numbers in data:
        if can_be_solved(
            expected_result=expected_result,
            numbers=numbers,
            operators=[
                lambda x, y: x * y,
                lambda x, y: x + y,
                lambda x, y: int(f"{x}{y}"),
            ],
        ):
            result += expected_result

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 3_749
    assert solve_part_two(data) == 11_387


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

