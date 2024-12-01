"""Day 01"""
from collections import Counter


T_Data = tuple[list[int], list[int]]


def read_input(file: str) -> T_Data:
    left, right = [], []

    with open(file, "r") as fin:
        for line in fin:
            parts = line.strip().split(" ")
            left.append(int(parts[0]))
            right.append(int(parts[-1]))

    return left, right


def compute_sum_of_distances(data: T_Data) -> int:
    left, right = data
    return sum([
        abs(x - y)
        for x, y in zip(sorted(left), sorted(right))
    ])


def compute_similarity_score(data: T_Data) -> int:
    left, right = data

    n_occurrences = Counter(right)

    return sum([
        num * n_occurrences[num]
        for num in left
    ])


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert compute_sum_of_distances(data) == 11
    assert compute_similarity_score(data) == 31


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = compute_sum_of_distances(data)
    print("Part one:", solution_one)

    solution_two = compute_similarity_score(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

