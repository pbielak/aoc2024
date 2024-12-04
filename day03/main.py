"""Day 03"""
import re


T_Memory = str


def read_input(file: str) -> T_Memory:
    with open(file, "r") as fin:
        return fin.read()


def run_multiplications(memory: T_Memory) -> int:
    result = 0

    for x, y in re.findall("mul\((\d{1,3})\,(\d{1,3})\)", memory):
        result += int(x) * int(y)

    return result


def run_multiplications_with_conditionals(memory: T_Memory) -> int:
    result = 0
    enabled = True

    for token in re.findall(
        pattern="(?P<name>mul|do|don't)\((?:(\d{1,3})\,(\d{1,3}))?\)",
        string=memory,
    ):
        if enabled and token[0] == "mul":
            result += int(token[1]) * int(token[2])
        elif token[0] == "do":
            enabled = True
        elif token[0] == "don't":
            enabled = False

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert run_multiplications(data) == 161

    data = read_input("data/example2.txt")
    assert run_multiplications_with_conditionals(data) == 48


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = run_multiplications(data)
    print("Part one:", solution_one)

    solution_two = run_multiplications_with_conditionals(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

