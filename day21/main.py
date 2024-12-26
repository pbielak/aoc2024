"""Day 21"""
from collections import defaultdict

T_Data = list[str]
T_KeypadMoves = dict[str, dict[str, str]]


"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
DOOR_KEYPAD_MOVES: T_KeypadMoves = {
    "A": {
        "0": "<",
        "1": "^<<", "2": "<^", "3": "^",
        "4": "^^<<", "5": "^^<", "6": "^^",
        "7": "^^^<<", "8": "^^^<", "9": "^^^",
    },
    "0": {
        "A": ">",
        "1": "^<", "2": "^", "3": "^>",
        "4": "^^<", "5": "^^", "6": "^^>",
        "7": "^^^<", "8": "^^^", "9": "^^^>",
    },
    "1": {
        "0": ">v", "A": ">>v",
        "2": ">", "3": ">>",
        "4": "^", "5": "^>", "6": "^>>",
        "7": "^^", "8": "^^>", "9": "^^>>",
    },
    "2": {
        "0": "v", "A": "v>",
        "1": "<", "3": ">",
        "4": "^<", "5": "^", "6": "^>",
        "7": "^^<", "8": "^^", "9": "^^>",
    },
    "3": {
        "0": "<v", "A": "v",
        "1": "<<", "2": "<",
        "4": "<<^", "5": "<^", "6": "^",
        "7": "<<^^", "8": "<^^", "9": "^^",
    },
    "4": {
        "0": ">vv", "A": ">>vv",
        "1": "v", "2": "v>", "3": "v>>",
        "5": ">", "6": ">>",
        "7": "^", "8": "^>", "9": "^>>",
    },
    "5": {
        "0": "vv", "A": "vv>",
        "1": "v<", "2": "v", "3": "v>",
        "4": "<", "6": ">",
        "7": "^<", "8": "^", "9": "^>",
    },
    "6": {
        "0": "<vv", "A": "vv",
        "1": "<<v", "2": "<v", "3": "v",
        "4": "<<", "5": "<",
        "7": "<<^", "8": "<^", "9": "^",
    },
    "7": {
        "0": ">vvv", "A": ">>vvv",
        "1": "vv", "2": "vv>", "3": "vv>>",
        "4": "v", "5": "v>", "6": "v>>",
        "8": ">", "9": ">>",
    },
    "8": {
        "0": "vvv", "A": "vvv>",
        "1": "vv<", "2": "vv", "3": "vv>",
        "4": "v<", "5": "v", "6": "v>",
        "7": "<", "9": ">",
    },
    "9": {
        "0": "<vvv", "A": "vvv",
        "1": "<<vv", "2": "<vv", "3": "vv",
        "4": "<<v", "5": "<v", "6": "v",
        "7": "<<", "8": "<",
    },
}

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
ROBOT_KEYPAD_MOVES: T_KeypadMoves = {
    "A": {"^": "<", "<": "v<<", "v": "<v", ">": "v"},
    "^": {"A": ">", "<": "v<", "v": "v", ">": "v>"},
    "v": {"A": "^>", "^": "^", "<": "<", ">": ">"},
    "<": {"A": ">>^", "^": ">^", "v": ">", ">": ">>"},
    ">": {"A": "^", "^": "<^", "v": "<", "<": "<<"},
}


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [line.strip() for line in fin.readlines()]


def get_seq(keypad_moves: T_KeypadMoves, code: str) -> list[str]:
    seq = []
    
    code = "A" + code

    for idx in range(len(code) - 1):
        src = code[idx]
        dst = code[idx + 1]

        if src == dst:
            seq.append("A")
        else:
            seq.append(keypad_moves[src][dst] + "A")

    return seq


def solve_part_one(data: T_Data) -> int:
    result = 0

    for code in data:
        door_seq = get_seq(DOOR_KEYPAD_MOVES, code)
        robot_seq = get_seq(ROBOT_KEYPAD_MOVES, ''.join(door_seq))
        my_seq = get_seq(ROBOT_KEYPAD_MOVES, ''.join(robot_seq))

        code_num = int(''.join(c for c in code if c.isdigit()))

        result += code_num * len(''.join(my_seq))

    return result


def solve_part_two(data: T_Data, num_robots: int = 25) -> int:
    result = 0

    for code in data:
        seq = get_seq(DOOR_KEYPAD_MOVES, code)

        counts = defaultdict(int)
        for s in seq:
            counts[s] += 1

        for _ in range(num_robots):
            new_counts = defaultdict(int)
            for _code, cnt in counts.items():
                for s in get_seq(ROBOT_KEYPAD_MOVES, _code):
                    new_counts[s] += cnt

            counts = new_counts

        code_num = int(''.join(c for c in code if c.isdigit()))
        seq_len = sum(len(k) * v for k, v in new_counts.items())

        result += code_num * seq_len

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 126_384
    assert solve_part_two(data, num_robots=2) == 126_384


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

