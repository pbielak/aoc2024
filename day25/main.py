"""Day 25"""
T_Block = list[list[str]]
T_Data = tuple[list[T_Block], list[T_Block]]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        locks = []
        keys = []
        
        for block in fin.read().strip().split("\n\n"):
            block = [list(line) for line in block.split("\n")]
            if block[0][0] == ".":  # is key
                keys.append(block)
            else:
                locks.append(block)

        return locks, keys


def to_height(block: T_Block) -> list[int]:
    width, height = len(block[0]), len(block)

    out = []
    for col in range(width):
        vals = [block[y][col] for y in range(height)]
        out.append(vals.count("#") - 1)

    return out


def solve_part_one(data: T_Data) -> int:
    locks, keys = data

    lock_heights = [(to_height(lock), len(lock) - 1) for lock in locks]
    key_heights = [to_height(key) for key in keys]

    result = 0
    for lock, max_height in lock_heights:
        for key in key_heights:
            sums = [lh + kh for lh, kh in zip(lock, key)]
            if any(s >= max_height for s in sums):
                continue

            result += 1

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 3


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)


if __name__ == "__main__":
    main()

