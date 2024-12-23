"""Day 18"""
import heapq
import sys
from itertools import product

T_Position = tuple[int, int]
T_Data = list[T_Position]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [
            tuple(int(c) for c in line.split(","))
            for line in fin.readlines()
        ]


def solve_part_one(
    data: T_Data,
    grid_size: int = 71,
    num_bytes: int = 1024,
) -> int:
    grid = [["."] * grid_size for _ in range(grid_size)]

    for x, y in data[:num_bytes]:
        grid[y][x] = "#"

    # Dijkstra
    start_pos = (0, 0)
    end_pos = (grid_size - 1, grid_size - 1)

    Q = []
    dists = {}

    for x, y in product(range(grid_size), repeat=2):
        if grid[y][x] == "#":
            continue

        dists[(x, y)] = sys.maxsize

    Q.append((0, start_pos))
    dists[start_pos] = 0

    while Q:
        dist_u, u = heapq.heappop(Q)

        if u == end_pos:
            break

        if dist_u > dists[u]:
            continue

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_x, new_y = u[0] + dx, u[1] + dy

            if not (0 <= new_x < grid_size):
                continue

            if not (0 <= new_y < grid_size):
                continue

            if grid[new_y][new_x] == "#":
                continue

            alt = dist_u + 1
            if alt < dists[(new_x, new_y)]:
                dists[(new_x, new_y)] = alt
                heapq.heappush(Q, (alt, (new_x, new_y)))

    result = dists[end_pos]

    return result


def solve_part_two(
    data: T_Data,
    grid_size: int = 71,
    num_bytes: int = 1024,
) -> int:
    for idx in range(num_bytes, len(data)):
        num_steps = solve_part_one(data, grid_size, num_bytes=idx)
        if num_steps == sys.maxsize:
            return data[idx - 1]


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data, grid_size=7, num_bytes=12) == 22
    assert solve_part_two(data, grid_size=7, num_bytes=12) == (6, 1)


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

