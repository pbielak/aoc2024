"""Day 10"""
import heapq
import sys

from collections import defaultdict


T_Data = list[list[int]]
T_Node = tuple[int, int, int]
T_Adj = dict[T_Node, list[T_Node]]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [
            [int(value) for value in line.strip()]
            for line in fin.readlines()
        ]


def to_graph(data: T_Data) -> tuple[list[T_Node], T_Adj]:
    nodes = []
    adj = defaultdict(list)

    width, height = len(data[0]), len(data)
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            node = (x, y, value)
            nodes.append(node)

            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if (
                    0 <= (x + dx) < width
                    and 0 <= (y + dy) < height
                    and data[y + dy][x + dx] == value + 1
                ):
                    neighbor = (x + dx, y + dy, data[y + dy][x + dx])
                    adj[node].append(neighbor)

    return nodes, adj


class NodePriorityQueue:

    def __init__(self):
        self._nodes_pq = []

    def add(self, node: T_Node, weight: int):
        heapq.heappush(self._nodes_pq, (weight, node))

    def pop(self) -> tuple[int, T_Node]:
        return heapq.heappop(self._nodes_pq)

    def __len__(self) -> int:
        return len(self._nodes_pq)


def dijkstra(
    nodes: list[T_Node],
    adj: T_Adj,
    start_node: T_Node,
) -> dict[T_Node, int]:
    Q = NodePriorityQueue()

    dist = {}

    for v in nodes:
        dist[v] = sys.maxsize

    dist[start_node] = 0
    Q.add(node=start_node, weight=0)

    while len(Q) > 0:
        dist_u, u = Q.pop()

        if dist_u > dist[u]:
            continue

        for v in adj[u]:
            alt = dist_u + 1
            if alt < dist[v]:
                dist[v] = alt
                Q.add(node=v, weight=alt)

    return dist


def solve_part_one(data: T_Data) -> int:
    result = 0

    nodes, adj = to_graph(data)
    
    start_nodes = [node for node in nodes if node[2] == 0]

    for sn in start_nodes:
        dists = dijkstra(nodes, adj, start_node=sn)
        end_dists = {
            n: dists[n]
            for n in nodes
            if dists[n] < sys.maxsize and n[2] == 9
        }

        result += len(end_dists)

    return result


def dfs(
    node: T_Node,
    adj: dict[T_Node, list[T_Node]],
    visited: set[T_Node],
) -> int:
    if node[2] == 9:
        return 1
    
    result = 0
    for neighbor in adj[node]:
        if neighbor in visited:
            continue
        result += dfs(neighbor, adj, {*visited, neighbor})

    return result


def solve_part_two(data: T_Data) -> int:
    result = 0

    nodes, adj = to_graph(data)

    start_nodes = [node for node in nodes if node[2] == 0]

    for sn in start_nodes:
        rating = dfs(node=sn, adj=adj, visited={sn})
        result += rating

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 36
    assert solve_part_two(data) == 81


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

