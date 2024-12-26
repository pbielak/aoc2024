"""Day 22"""
T_Data = list[int]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [int(line.strip()) for line in fin.readlines()]


def pseudorandom_step(secret: int) -> int:
    def mix(x: int, y: int) -> int:
        return x ^ y

    def prune(x: int) -> int:
        return x % 16_777_216

    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))

    return secret


def get_prng_seq(seed: int, steps: int = 2_000) -> list[int]:
    nums = [seed]
    for _ in range(steps):
        nums.append(pseudorandom_step(nums[-1]))

    return nums


def solve_part_one(data: T_Data) -> int:
    result = 0

    for num in data:
        result += get_prng_seq(num)[-1]

    return result


def get_diff(prices: list[int]) -> list[int]:
    return [a - b for a, b in zip(prices[1:], prices[:-1])]


def compute_changes_lookup(
    prices: list[int],
) -> dict[tuple[int, int, int, int], int]:
    diff = get_diff(prices)
    n = 4

    out = {}

    for idx in range(len(diff) - n):
        change = tuple(diff[idx:idx + n])

        if change in out.keys():
            continue

        out[change] = idx + n

    return out



def solve_part_two(data: T_Data) -> int:
    prices = [
        [n % 10 for n in get_prng_seq(num)]
        for num in data
    ]

    changes2idxs = [compute_changes_lookup(p) for p in prices]

    unique = set(
        k
        for c2i in changes2idxs
        for k in c2i.keys()
    )

    best = 0
    for a, b, c, d in unique:
        current_best = 0

        for p, c2i in zip(prices, changes2idxs):
            if (a, b, c, d) in c2i:
                idx = c2i[(a, b, c, d)]
                current_best += p[idx]

        best = max(best, current_best)

    return best


def run_tests() -> None:
    # Small example tests
    seq = get_prng_seq(123, steps=10)
    assert seq == [
        123,
        15_887_950,
        16_495_136,
        527_345,
        704_524,
        1_553_684,
        12_683_156,
        11_100_544,
        12_249_484,
        7_753_432,
        5_908_254,
    ]
    
    prices = [n % 10 for n in seq[:10]]
    assert prices == [3, 0, 6, 5, 4, 4, 6, 4, 4, 2]

    diff = get_diff(prices)
    assert diff == [-3, 6, -1, -1, 0, 2, -2, 0, -2]

    # Large example tests
    assert solve_part_one([1, 10, 100, 2024]) == 37_327_623
    assert solve_part_two([1, 2, 3, 2024]) == 23



def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

