"""Day 24"""
from copy import deepcopy

T_Wires = dict[str, int]
T_Gate = tuple[str, str, str, str]
T_Data = tuple[T_Wires, list[T_Gate]]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        raw_wires, raw_gates = fin.read().strip().split("\n\n")

        wires = {}
        for line in raw_wires.split("\n"):
            wire, state = line.strip().split(": ")
            wires[wire] = int(state)

        gates = []
        for line in raw_gates.split("\n"):
            w1, gtype, w2, out = line.strip().replace(" -> ",  " ").split(" ")
            gates.append((w1, gtype, w2, out))

        return wires, gates


def solve_part_one(data: T_Data) -> int:
    wires, gates = deepcopy(data)

    Q = gates[:]

    while Q:
        w1, gtype, w2, out = Q.pop(0)

        if w1 in wires and w2 in wires:
            if gtype == "AND":
                wires[out] = wires[w1] & wires[w2]
            elif gtype == "OR":
                wires[out] = wires[w1] | wires[w2]
            elif gtype == "XOR":
                wires[out] = wires[w1] ^ wires[w2]
        else:
            Q.append((w1, gtype, w2, out))

    z_keys = sorted([w for w in wires if "z" in w], reverse=True)

    result = int(''.join(str(wires[z]) for z in z_keys), base=2)

    return result


def solve_part_two(data: T_Data) -> int:
    wires, gates = deepcopy(data)

    for i in range(45):
        ws = {k: 0 for k, _ in wires.items()}

        for x_i, y_i, z_i in (
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 0),
        ):
            ws[f"x{i:02d}"] = x_i
            ws[f"y{i:02d}"] = y_i

            res = solve_part_one((ws, gates)) >> i
            actual_z_i = res % 2

            if z_i != actual_z_i:
                print(f"[{i}] {(x_i, y_i)} :: z_i wrong")

    wrong_wires = [
        # z18
        "z18", "hmt", 
        # z27
        "z27", "bfq",
        # z31
        "z31", "hkh",
        # z39
        "fjp", "bng",
    ]
    return ",".join(sorted(wrong_wires))


    # Print graphviz
    # for w1, gtype, w2, out in gates:
    #     print(f"""
    #         {w1} -> {gtype}_{w1}_{w2};
    #         {w2} -> {gtype}_{w1}_{w2};
    #         {gtype}_{w1}_{w2} -> {out};
    #     """)


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 2_024


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

