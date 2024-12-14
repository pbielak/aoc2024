"""Day 14"""
import os
import re
import sys
from collections import defaultdict

import numpy as np
from PIL import Image


T_Vec2D = tuple[int, int]
T_Robot = tuple[T_Vec2D, T_Vec2D]
T_Data = list[T_Robot]


def read_input(file: str) -> T_Data:
    data = []

    with open(file, "r") as fin:
        for line in fin.readlines():
            px, py, vx, vy = re.match(
                "p=(\d+),(\d+) v=(-?\d+),(-?\d+)",
                line.strip(),
            ).groups()

            p = (int(px), int(py))
            v = (int(vx), int(vy))

            data.append((p, v))

    return data


def simulate_robots(
    data: T_Data,
    width: int,
    height: int,
    num_seconds: int,
) -> dict[T_Vec2D, int]:
    out_pos = defaultdict(int)

    for (px, py), (vx, vy) in data:
        x = (px + num_seconds * vx) % width
        y = (py + num_seconds * vy) % height

        out_pos[(x, y)] += 1

    return out_pos


def compute_safety_factor(
    pos: dict[T_Vec2D, int],
    width: int,
    height: int,
) -> int:
    quadrants = [0, 0, 0, 0]

    for (x, y), count in pos.items():
        if x < width // 2 and y < height // 2:
            quadrants[0] += count
        elif x > width // 2 and y < height // 2:
            quadrants[1] += count
        elif x < width // 2 and y > height // 2:
            quadrants[2] += count
        elif x > width // 2 and y > height // 2:
            quadrants[3] += count

    safety_factor = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
    return safety_factor


def solve_part_one(data: T_Data, width: int, height: int) -> int:
    out_pos = simulate_robots(data, width, height, num_seconds=100)
    result = compute_safety_factor(out_pos, width, height)

    return result


def solve_part_two(data: T_Data) -> int:
    width, height = 101, 103
    for i in range(1, 10_000 + 1):
        out_pos = simulate_robots(data, width, height, num_seconds=i)

        arr = np.zeros((width, height), dtype=np.uint8)

        for (x, y), count in out_pos.items():
            arr[x, y] = 255 * min(count, 1)

        img = Image.fromarray(arr.T, mode="L")
        img.save(f"imgs/{i}.bmp")
        img.save(f"tmp_imgs/{i}.bmp")

        if i % 10 == 0:
            print("Running magick")
            os.system(f"magick montage -background gray -tile x2 tmp_imgs/* grid/{i}.png")
            os.system("rm -r tmp_imgs/")
            os.system("mkdir tmp_imgs/")


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data, width=11, height=7) == 12


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data, width=101, height=103)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

