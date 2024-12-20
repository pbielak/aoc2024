"""Day 15"""
from copy import deepcopy
from typing import Literal


T_Vec2D = tuple[int, int]
T_Instruction = Literal["<", "^", ">", "v"]
T_Map = list[list[str]]
T_Data = tuple[T_Map, list[T_Instruction]]

DIRECTIONS = {
    "<": (-1, 0),
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
}


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        raw_map, raw_instructions = fin.read().strip().split("\n\n")

        map_ = [list(line) for line in raw_map.split("\n")]
        instructions = [
            instruction
            for line in raw_instructions.split("\n")
            for instruction in line
        ]

        return map_, instructions


def get_robot_position(map_: T_Map) -> T_Vec2D:
    for y, line in enumerate(map_):
        for x, value in enumerate(line):
            if value == "@":
                return x, y


def move(map_: T_Map, src: T_Vec2D, dst: T_Vec2D) -> None:
    x1, y1 = src
    x2, y2 = dst

    map_[y1][x1], map_[y2][x2] = map_[y2][x2], map_[y1][x1]


def try_to_move_box(map_: T_Map, pos: T_Vec2D, delta: T_Vec2D) -> None:
    x, y = pos
    dx, dy = delta

    new_x, new_y = x + dx, y + dy

    if map_[new_y][new_x] == ".":
        move(map_, (x, y), (new_x, new_y))
    elif map_[new_y][new_x] == "#":
        pass
    elif map_[new_y][new_x] == "O":
        try_to_move_box(map_, (new_x, new_y), delta)

        if map_[new_y][new_x] == ".":
            move(map_, (x, y), (new_x, new_y))


def solve_part_one(data: T_Data) -> int:
    map_, instructions = deepcopy(data)
    robot_x, robot_y = get_robot_position(map_)

    for inst in instructions:
        dx, dy = DIRECTIONS[inst]

        new_x, new_y = robot_x + dx, robot_y + dy

        if map_[new_y][new_x] == ".":  # Move to the next position
            move(map_, (robot_x, robot_y), (new_x, new_y))
            robot_x, robot_y = new_x, new_y
        elif map_[new_y][new_x] == "#":  # Blocked path - do nothing
            pass
        elif map_[new_y][new_x] == "O":  # Box - check if can be moved
            try_to_move_box(map_, (new_x, new_y), (dx, dy))

            if map_[new_y][new_x] == ".":  # Box was moved
                move(map_, (robot_x, robot_y), (new_x, new_y))
                robot_x, robot_y = new_x, new_y
        
    gps = [
        100 * y + x
        for y, line in enumerate(map_)
        for x, value in enumerate(line)
        if value == "O"
    ]
    result = sum(gps)

    return result


def enlarge_map(map_: T_Map) -> T_Map:
    _mapping = {
        "#": ["#", "#"],
        "O": ["[", "]"],
        ".": [".", "."],
        "@": ["@", "."],
    }

    out = [
        [
            c
            for value in line
            for c in _mapping[value]
        ]
        for line in map_
    ]
    return out


class BigBox:
    
    def __init__(self, x: int, y: int, value: str):
        self.value = value
        if self.value == "[":
            self.pos_left = (x, y)
            self.pos_right = (x + 1, y)
        elif self.value == "]":
            self.pos_left = (x - 1, y)
            self.pos_right = (x, y)
        else:
            raise RuntimeError(f"Unknown tile: {self.value}")

    def can_be_moved(
        self,
        dx: int,
        dy: int,
        boxes: dict[T_Vec2D, "BigBox"],
        walls: set[T_Vec2D],
    ) -> bool:
        lx, ly = self.pos_left
        rx, ry = self.pos_right

        if dx == -1:  # Move left
            if (lx - 1, ly) in walls:
                return False

            if (lx - 1, ly) in boxes:
                return boxes[(lx - 1, ly)].can_be_moved(dx, dy, boxes, walls)

            return True

        if dx == 1:  # Move right
            if (rx + 1, ry) in walls:
                return False

            if (rx + 1, ry) in boxes:
                return boxes[(rx + 1, ry)].can_be_moved(dx, dy, boxes, walls)

            return True

        if dy != 0:  # Move up/down
            if (lx, ly + dy) in walls or (rx, ry + dy) in walls:
                return False

            can_be_moved = True
            if (lx, ly + dy) in boxes:
                can_be_moved = boxes[(lx, ly + dy)].can_be_moved(dx, dy, boxes, walls)

            if (rx, ry + dy) in boxes:
                can_be_moved = can_be_moved and boxes[(rx, ry + dy)].can_be_moved(dx, dy, boxes, walls)

            return can_be_moved

        raise RuntimeError("can_be_moved in illegal state")

    def move(
        self,
        dx: int,
        dy: int,
        boxes: dict[T_Vec2D, "BigBox"],
    ) -> None:
        lx, ly = self.pos_left
        rx, ry = self.pos_right
        value = self.value

        boxes.pop(self.pos_left)
        boxes.pop(self.pos_right)

        if (lx + dx, ly + dy) in boxes:
            boxes[(lx + dx, ly + dy)].move(dx, dy, boxes)

        if (rx + dx, ry + dy) in boxes:
            boxes[(rx + dx, ry + dy)].move(dx, dy, boxes)

        boxes[(lx + dx, ly + dy)] = BigBox(lx + dx, ly + dy, "[")
        boxes[(rx + dx, ry + dy)] = BigBox(rx + dx, ry + dy, "]")

    def __repr__(self) -> str:
        return f"Box('['={self.pos_left},']'={self.pos_right})"


def solve_part_two(data: T_Data) -> int:
    map_, instructions = deepcopy(data)
    map_ = enlarge_map(map_)
    robot_x, robot_y = get_robot_position(map_)

    boxes = {
        (x, y): BigBox(x, y, value)
        for y, line in enumerate(map_)
        for x, value in enumerate(line)
        if value in ("[", "]")
    }

    walls = set(
        (x, y)
        for y, line in enumerate(map_)
        for x, value in enumerate(line)
        if value == "#"
    )

    for inst in instructions:
        dx, dy = DIRECTIONS[inst]

        new_x, new_y = robot_x + dx, robot_y + dy

        if (new_x, new_y) in boxes:
            if boxes[(new_x, new_y)].can_be_moved(dx, dy, boxes, walls):
                boxes[(new_x, new_y)].move(dx, dy, boxes)
                robot_x, robot_y = new_x, new_y
        elif (new_x, new_y) in walls:
            pass
        else:  # Move to the next position
            robot_x, robot_y = new_x, new_y
        
    gps = [
        100 * box.pos_left[1] + box.pos_left[0]
        for box in boxes.values()
        if box.value == "["
    ]
    result = sum(gps)

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 2028

    data = read_input("data/example2.txt")
    assert solve_part_one(data) == 10_092
    assert solve_part_two(data) == 9021


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

