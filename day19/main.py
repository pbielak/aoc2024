"""Day 19"""
from functools import lru_cache


T_Data = tuple[list[str], list[str]]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        raw_towels, raw_designs = fin.read().strip().split("\n\n")

        return raw_towels.split(", "), raw_designs.split("\n")


@lru_cache
def count_towel_sequences(towels: tuple[str], design: str) -> int:
    count = 0

    for towel in towels:
        if not design.startswith(towel):
            continue

        if design == towel:
            count += 1
            continue

        count += count_towel_sequences(towels, design[len(towel):])

    return count


def solve_part_one(data: T_Data) -> int:
    towels, designs = data

    result = 0

    for design in designs:
        useful_towels = tuple(towel for towel in towels if towel in design)
        count = count_towel_sequences(useful_towels, design)

        if count > 0:
            result += 1

    return result


def solve_part_two(data: T_Data) -> int:
    towels, designs = data

    result = 0

    for design in designs:
        useful_towels = tuple(towel for towel in towels if towel in design)
        result += count_towel_sequences(useful_towels, design)

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 6
    assert solve_part_two(data) == 16


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

