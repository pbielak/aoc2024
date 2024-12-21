"""Day 16"""
import heapq
import sys
from collections import defaultdict
from typing import Literal


T_Map = list[list[str]]
T_Position = tuple[int, int]
T_Direction = Literal["N", "S", "E", "W"]
T_Node = T_Position
T_Adj = dict[T_Node, list[tuple[T_Node, T_Direction]]]

_DIRECTIONS: dict[T_Direction, T_Position] = {
    "E": (1, 0),
    "W": (-1, 0),
    "S": (0, 1),
    "N": (0, -1),
}


def read_input(file: str) -> T_Map:
    with open(file, "r") as fin:
        return [list(line.strip()) for line in fin.readlines()]


def find_start_end_positions(map_: T_Map) -> tuple[T_Position, T_Position]:
    start_pos = None
    end_pos = None

    for y, line in enumerate(map_):
        for x, value in enumerate(line):
            if value == "S":
                start_pos = x, y
            elif value == "E":
                end_pos = x, y

    assert start_pos is not None
    assert end_pos is not None

    return start_pos, end_pos


def build_graph(map_: T_Map) -> tuple[list[T_Node], T_Adj]:
    nodes = []
    adj = defaultdict(list)

    width, height = len(map_[0]), len(map_)
    for y, line in enumerate(map_):
        for x, value in enumerate(line):
            nodes.append((x, y))

            for name, (dx, dy) in _DIRECTIONS.items():
                new_x, new_y = x + dx, y + dy

                if not (0 <= new_x < width):
                    continue

                if not (0 <= new_y < height):
                    continue

                if map_[new_y][new_x] == "#":
                    continue

                adj[(x, y)].append(((new_x, new_y), name))

    return nodes, adj


def custom_dijkstra(
    nodes: list[T_Node],
    adj: T_Adj,
    start_node: T_Node,
    end_node: T_Node,
) -> int:
    Q = []
    dist = {}

    for v in nodes:
        for d in _DIRECTIONS.keys():
            dist[(v, d)] = sys.maxsize

    dist[(start_node, "E")] = 0
    heapq.heappush(Q, (0, (start_node, "E")))

    while len(Q) > 0:
        dist_u, (u, u_dir) = heapq.heappop(Q)
        
        if u == end_node:
            return dist_u

        if dist_u > dist[(u, u_dir)]:
            continue

        for v, v_dir in adj[u]:
            cost = 1 + 1000 * int(u_dir != v_dir)
            alt = dist_u + cost
            if alt < dist[(v, v_dir)]:
                dist[(v, v_dir)] = alt
                heapq.heappush(Q, (alt, (v, v_dir)))

    raise RuntimeError("custom_dijkstra: did not reach end node")


def solve_part_one(map_: T_Map) -> int:
    start_pos, end_pos = find_start_end_positions(map_)
    nodes, adj = build_graph(map_)

    cost = custom_dijkstra(
        nodes,
        adj,
        start_node=start_pos,
        end_node=end_pos,
    )

    return cost


def solve_part_two(map_: T_Map) -> int:
    result = 0

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 7_036
    # assert solve_part_two(data) == ...

    data = read_input("data/example2.txt")
    assert solve_part_one(data) == 11_048
    # assert solve_part_two(data) == ...

    assert solve_part_one(read_input("data/example3.txt")) == 21_148
    assert solve_part_one(read_input("data/example4.txt")) == 4_013


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

