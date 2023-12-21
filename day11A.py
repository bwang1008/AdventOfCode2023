import time
from typing import List, Tuple

from loguru import logger

DEBUG: bool = False


def find_dist_between_two_galaxies(
    galaxy_a: Tuple[int, int],
    galaxy_b: Tuple[int, int],
    empty_rows: List[int],
    empty_cols: List[int],
) -> int:
    def find_lower_bound(search_space: List[int], desired_number_in_range: int) -> int:
        """Given non-decreasing list of ints and a desired int, find index of lowest number
        that is greater-or-equal to desired_number_in_range.

        Ex: [1, 3, 7, 10] and desired_number_in_range = 5 would return 2, because search_space[2] = 7 >= 5
        """
        low: int = 0
        high: int = len(search_space) - 1

        while low <= high:
            mid: int = (low + high) // 2
            if search_space[mid] < desired_number_in_range:
                low = mid + 1
            else:
                high = mid - 1

        return low

    def find_upper_bound(search_space: List[int], desired_number_in_range: int) -> int:
        """Given non-decreasing list of ints and a desired int, find index of highest number
        that is less-than-or-equal to desired_number_in_range.

        Ex: [1, 3, 7, 10] and desired_number_in_range = 5 would return 1, because search_space[1] = 3 <= 5
        """
        low: int = 0
        high: int = len(search_space) - 1

        while low <= high:
            mid: int = (low + high) // 2
            if search_space[mid] > desired_number_in_range:
                high = mid - 1
            else:
                low = mid + 1

        return high

    row_lower_bound_index: int = find_lower_bound(
        empty_rows, min(galaxy_a[0], galaxy_b[0])
    )
    row_upper_bound_index: int = find_upper_bound(
        empty_rows, max(galaxy_a[0], galaxy_b[0])
    )
    col_lower_bound_index: int = find_lower_bound(
        empty_cols, min(galaxy_a[1], galaxy_b[1])
    )
    col_upper_bound_index: int = find_upper_bound(
        empty_cols, max(galaxy_a[1], galaxy_b[1])
    )

    num_empty_rows_between_galaxies: int = max(
        row_upper_bound_index - row_lower_bound_index + 1, 0
    )
    num_empty_cols_between_galaxies: int = max(
        col_upper_bound_index - col_lower_bound_index + 1, 0
    )

    return (
        abs(galaxy_b[0] - galaxy_a[0])
        + num_empty_rows_between_galaxies
        + abs(galaxy_b[1] - galaxy_a[1])
        + num_empty_cols_between_galaxies
    )


def find_sum_of_dist_between_every_two_galaxies(universe: List[str]) -> int:
    GALAXY_SYMBOL: str = "#"
    SPACE_SYMBOL: str = "."

    empty_rows: List[int] = []
    for index, row in enumerate(universe):
        if all(s == SPACE_SYMBOL for s in row):
            empty_rows.append(index)

    empty_cols: List[int] = []
    for index in range(len(universe[0])):
        if all(row[index] == SPACE_SYMBOL for row in universe):
            empty_cols.append(index)

    galaxy_indices: List[Tuple[int, int]] = []
    for row_index, row in enumerate(universe):
        for col_index, character in enumerate(row):
            if character == GALAXY_SYMBOL:
                galaxy_indices.append((row_index, col_index))

    total_dist: int = 0

    for index_1 in range(len(galaxy_indices)):
        for index_2 in range(index_1 + 1, len(galaxy_indices)):
            total_dist += find_dist_between_two_galaxies(
                galaxy_indices[index_1], galaxy_indices[index_2], empty_rows, empty_cols
            )

    return total_dist


def main() -> None:
    input_file: str = "inputs/day11.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    answer: int = find_sum_of_dist_between_every_two_galaxies(input_lines)
    logger.info(f"{answer=}")  # 9370588


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
