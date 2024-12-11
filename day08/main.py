"""Day 08"""
from collections import defaultdict
from itertools import product

T_Data = list[list[str]]
T_Position = tuple[int, int]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [list(line.strip()) for line in fin.readlines()]


def vec_shift(a: T_Position, b: T_Position, scale: int) -> T_Position:
    a_x, a_y = a
    b_x, b_y = b

    vec_x = b_x - a_x
    vec_y = b_y - a_y

    out_x = a_x + scale * vec_x
    out_y = a_y + scale * vec_y
    return out_x, out_y


def get_antinodes_locations(data: T_Data, scale: int) -> list[T_Position]:
    antinode_locations = []
    frequencies = defaultdict(list)

    for y, line in enumerate(data):
        for x, value in enumerate(line):
            if value == ".":
                continue

            frequencies[value].append((x, y))

    width, height = len(data[0]), len(data)

    for freq, antennas in frequencies.items():
        for a1, a2 in product(antennas, repeat=2):
            if a1 == a2:
                continue

            loc_x, loc_y = vec_shift(a1, a2, scale=scale)

            if loc_x < 0 or loc_x >= width:
                continue

            if loc_y < 0 or loc_y >= height:
                continue

            antinode_locations.append((loc_x, loc_y))

    return antinode_locations


def solve_part_one(data: T_Data) -> int:
    antinode_locations = get_antinodes_locations(data, scale=2)

    unique_locations = set(antinode_locations)
    return len(unique_locations)


def solve_part_two(data: T_Data) -> int:
    unique_locations = set()
    scale = 1
    
    while True:
        antinode_locations = get_antinodes_locations(data, scale=scale)
        if len(antinode_locations) == 0:
            break
        unique_locations.update(antinode_locations)
        scale += 1

    return len(unique_locations)


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 14
    assert solve_part_two(data) == 34


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

