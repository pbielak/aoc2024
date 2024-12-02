"""Day 02"""
T_Report = list[int]
T_Data = list[T_Report]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [
            [int(level) for level in report.split(" ")]
            for report in fin
        ]


def count_safe_reports(data: T_Data) -> int:
    return len([report for report in data if is_safe(report)])


def count_safe_reports_with_dampener(data: T_Data) -> int:
    num_safe = 0

    for report in data:
        if is_safe(report):
            num_safe += 1
            continue

        for idx in range(len(report)):
            modified_report = [*report[:idx], *report[idx + 1:]]
            if is_safe(modified_report):
                num_safe += 1
                break

    return num_safe


def is_safe(report: T_Report) -> bool:
    diffs = [a - b for a, b in zip(report[:-1], report[1:])]

    is_increasing = all(d > 0 for d in diffs)
    is_decreasing = all(d < 0 for d in diffs)
    is_bounded = all(1 <= abs(d) <= 3 for d in diffs)

    return is_bounded and (is_increasing or is_decreasing)


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert count_safe_reports(data) == 2
    assert count_safe_reports_with_dampener(data) == 4


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = count_safe_reports(data)
    print("Part one:", solution_one)

    solution_two = count_safe_reports_with_dampener(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

