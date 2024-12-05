"""Day 05"""
from functools import cmp_to_key


T_Rule = tuple[int, int]
T_Update = list[int]
T_Data = tuple[list[T_Rule], list[T_Update]]


def read_input(file: str) -> T_Data:
    rules = []
    updates = []

    with open(file, "r") as fin:
        raw_rules, raw_updates = fin.read().strip().split("\n\n")
        for rule in raw_rules.split("\n"):
            i, j = rule.split("|")
            rules.append((int(i), int(j)))

        for update in raw_updates.split("\n"):
            updates.append([int(page) for page in update.split(",")])

    return rules, updates


def is_correctly_ordered(rules: list[T_Rule], update: T_Update) -> bool:
    indices = dict(zip(update, range(len(update))))

    for a, b in rules:
        if a in update and b in update:  # This rule applies to the current update
            if indices[a] > indices[b]:  # If page ordering is wrong
                return False

    return True


def solve_part_one(data: T_Data) -> int:
    result = 0

    rules, updates = data

    for update in updates:
        if is_correctly_ordered(rules, update):
            result += update[len(update) // 2]

    return result


def solve_part_two(data: T_Data) -> int:
    result = 0

    rules, updates = data

    def _cmp_fn(a, b):
        if (a, b) in rules:
            return -1

        if a == b:
            return 0

        return 1

    wrongly_ordered = [
        update
        for update in updates
        if not is_correctly_ordered(rules, update)
    ]

    for wu in wrongly_ordered:
        update = sorted(wu, key=cmp_to_key(_cmp_fn))
        result += update[len(update) // 2]

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 143
    assert solve_part_two(data) == 123


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

