"""Day 23"""
import networkx as nx

T_Data = list[tuple[str, str]]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        out = []

        for line in fin.readlines():
            c1, c2 = line.strip().split("-")
            out.append((c1, c2))

        return out


def solve_part_one(data: T_Data) -> int:
    g = nx.Graph()
    g.add_edges_from(data)

    triangles = [x for x in nx.enumerate_all_cliques(g) if len(x) == 3]

    result = 0

    for a, b, c in triangles:
        if a.startswith("t") or b.startswith("t") or c.startswith("t"):
            result += 1

    return result


def solve_part_two(data: T_Data) -> str:
    g = nx.Graph()
    g.add_edges_from(data)

    max_clique = None
    max_clique_size = 0

    for clique in nx.enumerate_all_cliques(g):
        if len(clique) > max_clique_size:
            max_clique_size = len(clique)
            max_clique = clique

    return ",".join(sorted(max_clique))


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 7
    assert solve_part_two(data) == "co,de,ka,ta"


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

