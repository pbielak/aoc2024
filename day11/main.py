"""Day 11"""
from collections import defaultdict


T_Data = list[int]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [int(value) for value in fin.read().split(" ")]


def run_pebble_iteration(stones: T_Data) -> T_Data:
    out_stones = []

    for stone in stones:
        if stone == 0:
            out_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            digits = str(stone)
            mid = len(digits) // 2
            out_stones.append(int(digits[:mid]))
            out_stones.append(int(digits[mid:]))
        else:
            out_stones.append(stone * 2024)

    return out_stones


def solve_part_one(data: T_Data) -> int:
    stones = data.copy()
    for _ in range(25):
        stones = run_pebble_iteration(stones)

    return len(stones)


def solve_part_two(data: T_Data, num_blinks: int = 75) -> int:
    count = defaultdict(int)

    for stone in data:
        count[stone] = 1

    for i in range(num_blinks):
        new_count = defaultdict(int)
        for stone, c in count.items():
            out = run_pebble_iteration([stone])
            for o in out:
                new_count[o] += c

        count = new_count

    total_stones = sum(count.values())
    return total_stones


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 55_312
    assert solve_part_two(data, num_blinks=25) == 55_312


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

