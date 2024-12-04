"""Day 04"""
from itertools import product


T_Data = list[str]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [line.strip() for line in fin.readlines()]


def find_num_xmas(data: T_Data) -> int:
    counter = 0

    width, height = len(data[0]), len(data)

    deltas = [-1, 0, 1]
    word_len = 4

    for start_x, start_y in product(range(width), range(height)):
        if data[start_y][start_x] != "X":
            continue

        for dx, dy in product(deltas, repeat=2):
            indices = [
                (start_x + i * dx, start_y + i * dy)
                for i in range(word_len)
            ]

            if any(x < 0 or x >= width for x, _ in indices):
                continue

            if any(y < 0 or y >= height for _, y in indices):
                continue

            word = "".join(data[y][x] for x, y in indices)
            if word == "XMAS":
                counter += 1

    return counter


def find_num_crossed_mas(data: T_Data) -> int:
    counter = 0

    width, height = len(data[0]), len(data)

    for start_x, start_y in product(range(1, width - 1), range(1, height - 1)):
        diagonal = "".join([
            data[start_y - 1][start_x - 1],
            data[start_y][start_x],
            data[start_y + 1][start_x + 1],
        ])
        antidiagonal = "".join([
            data[start_y + 1][start_x - 1],
            data[start_y][start_x],
            data[start_y - 1][start_x + 1],
        ])

        if (
            data[start_y][start_x] == "A"
            and diagonal in ("MAS", "SAM")
            and antidiagonal in ("MAS", "SAM")
        ):
            counter += 1

    return counter


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert find_num_xmas(data) == 18
    assert find_num_crossed_mas(data) == 9


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = find_num_xmas(data)
    print("Part one:", solution_one)

    solution_two = find_num_crossed_mas(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

