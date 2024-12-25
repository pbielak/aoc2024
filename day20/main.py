"""Day 20"""
import heapq
import sys
from collections import defaultdict


T_Data = list[list[str]]
T_Position = tuple[int, int]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [list(line.strip()) for line in fin.readlines()]


def find_start_end_positions(grid: T_Data) -> tuple[T_Position, T_Position]:
    start_pos, end_pos = None, None

    for y, line in enumerate(grid):
        for x, value in enumerate(line):
            if value == "S":
                start_pos = (x, y)
            elif value == "E":
                end_pos = (x, y)

    assert start_pos is not None
    assert end_pos is not None

    return start_pos, end_pos


def dijkstra(
    grid: T_Data,
    start_pos: T_Position,
    end_pos: T_Position,
) -> tuple[dict[T_Position, int], dict[T_Position, T_Position]]:
    width, height = len(grid[0]), len(grid)

    Q = []
    dists = {}
    prev = {}

    for y, line in enumerate(grid):
        for x, value in enumerate(line):
            if value == ".":
                dists[(x, y)] = sys.maxsize
    dists[end_pos] = sys.maxsize

    Q.append((0, start_pos))
    dists[start_pos] = 0
    prev[start_pos] = None

    while Q:
        dist_u, (ux, uy) = heapq.heappop(Q)

        if (ux, uy) == end_pos:
            return dists, prev

        if dist_u > dists[(ux, uy)]:
            continue

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_x, new_y = ux + dx, uy + dy

            if not (0 <= new_x < width):
                continue

            if not (0 <= new_y < height):
                continue

            if grid[new_y][new_x] == "#":
                continue

            alt = dist_u + 1
            if alt < dists[(new_x, new_y)]:
                dists[(new_x, new_y)] = alt
                prev[(new_x, new_y)] = (ux, uy)
                heapq.heappush(Q, (alt, (new_x, new_y)))

    raise RuntimeError("Did not find end position")


def count_cheats(data: T_Data, max_cheat_duration: int) -> dict[int, int]:
    start_pos, end_pos = find_start_end_positions(data)
    _, prev = dijkstra(data, start_pos, end_pos)

    path = [end_pos]
    pos = end_pos
    while prev[pos] is not None:
        path = [prev[pos], *path]
        pos = prev[pos]

    count = defaultdict(int)

    for s_idx in range(len(path)):
        for t_idx in range(s_idx + 1, len(path)):
            sx, sy = path[s_idx]
            tx, ty = path[t_idx]

            dist = abs(sx - tx) + abs(sy - ty)

            if 2 <= dist <= max_cheat_duration:
                save_ps = t_idx - s_idx - dist
                if save_ps > 0:
                    count[save_ps] += 1

    return count


def solve_part_one(data: T_Data) -> int:
    result = 0

    cnt = count_cheats(data, max_cheat_duration=2)
    for save_ps, num_cheats in cnt.items():
        if save_ps >= 100:
            result += num_cheats

    return result


def solve_part_two(data: T_Data) -> int:
    result = 0

    cnt = count_cheats(data, max_cheat_duration=20)
    for save_ps, num_cheats in cnt.items():
        if save_ps >= 100:
            result += num_cheats

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert count_cheats(data, max_cheat_duration=2) == {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }
    
    counts_p2 = {
        save_ps: cnt
        for save_ps, cnt in count_cheats(data, max_cheat_duration=20).items()
        if save_ps >= 50
    }
    assert counts_p2 == {
        50: 32,
        52: 31,
        54: 29, 
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

