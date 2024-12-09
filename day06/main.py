"""Day 06"""
from copy import deepcopy


T_Data = list[list[str]]
T_Position = tuple[int, int]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [list(line.strip()) for line in fin.readlines()]


def get_guard_start_position(data: T_Data) -> T_Position:
    for y, line in enumerate(data):
        if "^" in line:
            start_y = y
            start_x = line.index("^")
            return start_x, start_y

    raise RuntimeError("Guard not found")


def run_guard_simulation(
    data: T_Data,
    start_x: int,
    start_y: int,
) -> tuple[int, bool]:
    guard_positions_with_directions = set()

    width, height = len(data[0]), len(data)
    dx, dy = 0, -1  # Move up
    guard_x, guard_y = start_x, start_y

    _right_turns = {
        (0, -1): (1, 0),
        (1, 0): (0, 1),
        (0, 1): (-1, 0),
        (-1, 0): (0, -1),
    }

    while True:
        guard_positions_with_directions.add((guard_x, guard_y, dx, dy))

        next_x, next_y = guard_x + dx, guard_y + dy

        # Stuck in loop
        if (next_x, next_y, dx, dy) in guard_positions_with_directions:
            return -1, True

        # Has left map
        if (
            next_x < 0 or next_x >= width
            or next_y < 0 or next_y >= height
        ):
            num_unique_positions = len({
                (x, y)
                for x, y, _, _ in guard_positions_with_directions
            })
            return num_unique_positions, False

        # In front of obstacle
        if data[next_y][next_x] == "#":
            dx, dy = _right_turns[(dx, dy)]
            continue

        # Go to the next position
        guard_x, guard_y = next_x, next_y


def solve_part_one(data: T_Data) -> int:
    guard_x, guard_y = get_guard_start_position(data)

    num_unique_positions, stuck_in_loop = run_guard_simulation(
        data=data,
        start_x=guard_x,
        start_y=guard_y,
    )

    assert not stuck_in_loop
    return num_unique_positions


def solve_part_two(data: T_Data) -> int:
    result = 0

    width, height = len(data[0]), len(data)
    guard_x, guard_y = get_guard_start_position(data)

    for x in range(width):
        for y in range(height):
            if data[y][x] in ("#", "^"):
                continue

            map_ = deepcopy(data)
            map_[y][x] = "#"

            _, stuck_in_loop = run_guard_simulation(
                data=map_,
                start_x=guard_x,
                start_y=guard_y,
            )

            if stuck_in_loop:
                result += 1

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 41
    assert solve_part_two(data) == 6


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

