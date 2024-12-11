"""Day 09"""
T_Data = str


def read_input(file: str) -> T_Data:
    with open(file, "r") as fin:
        return fin.read().strip()


def to_disk_layout(data: T_Data) -> list[str]:
    disk = []
    file_id = 0
    
    for idx, value in enumerate(data):
        if idx % 2 == 0:  # Data
            disk.extend([str(file_id)] * int(value))
            file_id += 1
        else:  # Free space
            disk.extend(["."] * int(value))

    return disk


def compute_checksum(disk: list[str]) -> int:
    checksum = 0

    for idx, value in enumerate(disk):
        if value == ".":
            continue
        checksum += idx * int(value)

    return checksum


def solve_part_one(data: T_Data) -> int:
    disk = to_disk_layout(data)

    # Defragment by single block
    left = disk.index(".")
    right = len(disk) - 1

    while left < right:
        while disk[left] != ".":
            left += 1
        while disk[right] == ".":
            right -= 1

        disk[left] = disk[right]
        disk[right] = "."

        left += 1
        right -= 1

    checksum = compute_checksum(disk)
    return checksum


def solve_part_two(data: T_Data) -> int:
    disk = to_disk_layout(data)

    # Defragment by whole blocks
    files = []  # (ID, start_idx, size)
    for file_id, file_size in enumerate(data[::2]):
        files.append((file_id, disk.index(str(file_id)), int(file_size)))

    free_spaces = []  # (start_idx, size)
    i = disk.index(".")
    while i < len(disk):
        start_idx = i
        while disk[i] == ".":
            i += 1

        free_spaces.append((start_idx, i - start_idx))

        while i < len(disk) and disk[i] != ".":
            i += 1

    # Move whole blocks and update free space info
    for file_id, file_start_idx, file_size in files[::-1]:
        selected_free_space_idx = next(
            (
                idx
                for idx, (_, fs_size) in enumerate(free_spaces)
                if fs_size >= file_size
            ),
            None,
        )

        if selected_free_space_idx is None:  # No free space that will fit file
            continue

        fs_start_idx, fs_size = free_spaces[selected_free_space_idx]

        if fs_start_idx > file_start_idx: # Ensure free space is to the left of the file
            continue

        disk[fs_start_idx:fs_start_idx + file_size] = disk[
            file_start_idx:file_start_idx + file_size
        ]
        disk[file_start_idx:file_start_idx + file_size] = ["."] * file_size

        new_fs_size = fs_size - file_size
        if new_fs_size == 0:
            free_spaces = [
                *free_spaces[:selected_free_space_idx],
                *free_spaces[selected_free_space_idx + 1:],
            ]
        else:
            free_spaces[selected_free_space_idx] = (fs_start_idx + file_size, new_fs_size)

    checksum = compute_checksum(disk)
    return checksum


def run_tests() -> None:
    data = read_input("data/example.txt")
    assert solve_part_one(data) == 1928
    assert solve_part_two(data) == 2858


def main() -> None:
    run_tests()

    data = read_input("data/input.txt")

    solution_one = solve_part_one(data)
    print("Part one:", solution_one)

    solution_two = solve_part_two(data)
    print("Part two:", solution_two)


if __name__ == "__main__":
    main()

