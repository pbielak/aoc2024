"""Day 12"""
T_Data = list[list[str]]
T_Position = tuple[int, int]


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return [list(line.strip()) for line in fin.readlines()]


def find_regions(data: T_Data) -> list[list[T_Position]]:
    regions = []

    visited: set[T_Position] = set()

    width, height = len(data[0]), len(data)

    def dfs(pos: T_Position) -> list[T_Position]:
        region = [pos]
        visited.add(pos)

        x, y = pos
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_x = x + dx
            new_y = y + dy

            new_pos = new_x, new_y

            if not (0 <= new_x < width):
                continue

            if not (0 <= new_y < height):
                continue

            if new_pos in visited:
                continue

            if data[new_y][new_x] == data[y][x]:
                region.extend(dfs(new_pos))

        return region

    for y, row in enumerate(data):
        for x, garden_type in enumerate(row):
            current_pos = (x, y)

            if current_pos in visited:
                continue

            regions.append(dfs(current_pos))

    return regions


def compute_perimeter(region: list[T_Position]) -> int:
    perimeter = 0

    tiles = set(region)

    for x, y in region:
        n_same_neighbors = 0

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if (x + dx, y + dy) in tiles:
                n_same_neighbors += 1

        perimeter += (4 - n_same_neighbors)

    return perimeter



def solve_part_one(data: T_Data) -> int:
    result = 0

    for region in find_regions(data):
        area = len(region)
        perimeter = compute_perimeter(region)

        result += area * perimeter

    return result



def compute_num_sides(region: list[T_Position]) -> int:
    tiles = set(region)

    _DIRECTIONS = {
        "UP": (0, -1),
        "DOWN": (0, 1),
        "LEFT": (-1, 0),
        "RIGHT": (1, 0),
        "TOP_LEFT": (-1, -1),
        "TOP_RIGHT": (1, -1),
        "BOTTOM_LEFT": (-1, 1),
        "BOTTOM_RIGHT": (1, 1),
    }

    num_corners = 0

    for x, y in region:
        def _in_region(direction: str) -> bool:
            dx, dy = _DIRECTIONS[direction]
            return (x + dx, y + dy) in tiles

        # Check for outer corners
        if not _in_region("LEFT") and not _in_region("UP"):
            num_corners += 1

        if not _in_region("RIGHT") and not _in_region("UP"):
            num_corners += 1

        if not _in_region("LEFT") and not _in_region("DOWN"):
            num_corners += 1

        if not _in_region("RIGHT") and not _in_region("DOWN"):
            num_corners += 1

        # Check for inner corners
        if _in_region("LEFT") and _in_region("UP") and not _in_region("TOP_LEFT"):
            num_corners += 1

        if _in_region("RIGHT") and _in_region("UP") and not _in_region("TOP_RIGHT"):
            num_corners += 1

        if _in_region("LEFT") and _in_region("DOWN") and not _in_region("BOTTOM_LEFT"):
            num_corners += 1

        if _in_region("RIGHT") and _in_region("DOWN") and not _in_region("BOTTOM_RIGHT"):
            num_corners += 1

    return num_corners


def solve_part_two(data: T_Data) -> int:
    result = 0

    for region in find_regions(data):
        area = len(region)
        num_sides = compute_num_sides(region)

        result += area * num_sides

    return result


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 140
    assert solve_part_two(data) == 80

    data = read_input("data/example2.txt")
    assert solve_part_one(data) == 772
    assert solve_part_two(data) == 436

    data = read_input("data/example3.txt")
    assert solve_part_two(data) == 236

    data = read_input("data/example4.txt")
    assert solve_part_two(data) == 368


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

