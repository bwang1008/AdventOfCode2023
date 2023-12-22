import time
from typing import List

from loguru import logger

DEBUG: bool = False

DAMAGED_SPRING: str = "#"
NORMAL_SPRING: str = "."
UNKNOWN: str = "?"


def group_up_completed(row: List[str]) -> List[int]:
    groups: List[int] = []

    curr_num = 0

    for c in row:
        if c == DAMAGED_SPRING:
            curr_num += 1
        else:
            if curr_num > 0:
                groups.append(curr_num)
            curr_num = 0

    if curr_num > 0:
        groups.append(curr_num)

    return groups


def try_all_possible_combinations(row: List[str], desired_groups: List[int]):
    logger.debug(f"try_all_possible_combinations({row=}, {desired_groups=}")
    num_unknown_that_are_damaged: int = sum(desired_groups) - len(
        [i for i in range(len(row)) if row[i] == DAMAGED_SPRING]
    )
    unknown_indices: List[int] = [i for i, v in enumerate(row) if v == UNKNOWN]

    logger.debug(f"{unknown_indices=} and {num_unknown_that_are_damaged=}")

    num_good_combinations: int = 0
    num_filled_in: int = 0

    def fill_in_one_position(row: List[str], index_of_unknown_indices: int) -> None:
        nonlocal num_good_combinations
        nonlocal num_filled_in

        if index_of_unknown_indices == len(unknown_indices):
            #  logger.debug(f'Reached end! Have {row=} with grouping {group_up_completed(row)}')
            if group_up_completed(row) == desired_groups:
                num_good_combinations += 1
            return

        curr_index: int = unknown_indices[index_of_unknown_indices]

        # fill in normal spring
        row[curr_index] = NORMAL_SPRING
        fill_in_one_position(row, 1 + index_of_unknown_indices)
        row[curr_index] = UNKNOWN

        if num_filled_in < num_unknown_that_are_damaged:
            # fill in damaged spring
            row[curr_index] = DAMAGED_SPRING
            num_filled_in += 1
            fill_in_one_position(row, 1 + index_of_unknown_indices)
            num_filled_in -= 1
            row[curr_index] = UNKNOWN

    fill_in_one_position(row, 0)

    logger.debug(f"Result: {num_good_combinations=}")

    return num_good_combinations


def main() -> None:
    input_file: str = "inputs/day12.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    answer: int = 0

    for line in input_lines:
        parts: List[str] = line.split(" ")
        row: List[str] = [s for s in parts[0]]
        desired_groups: List[int] = [int(s) for s in parts[1].split(",")]

        answer += try_all_possible_combinations(row, desired_groups)

    logger.info(f"{answer=}")  # 7017


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
