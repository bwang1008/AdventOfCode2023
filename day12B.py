import time
from typing import List, Optional

from loguru import logger

DEBUG: bool = False

DAMAGED_SPRING: str = "#"
NORMAL_SPRING: str = "."
UNKNOWN: str = "?"

INPUT_MULTIPLIER: int = 5

num_times_called_recursive_function: int = 0


def group_up_completed(row: List[str]) -> List[int]:
    """Given row of springs, count up the groups of damaged springs."""
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


def plausibly_works(row: List[str], desired_groups: List[int]) -> bool:
    """Check if a row of springs can possibly generate the list of desired groups
    of damaged springs.
    """

    # only read up to before first "?" spring
    unknown_index: int = -1
    for i, s in enumerate(row):
        if s == UNKNOWN:
            unknown_index = i
            break

    current_groups: List[int] = (
        group_up_completed(row)
        if unknown_index == -1
        else group_up_completed(row[:unknown_index])
    )

    if current_groups == desired_groups:
        return True
    if 0 == len(current_groups):
        return True

    if len(current_groups) > len(desired_groups):
        return False

    # if all question marks filled, this should not be the case
    if unknown_index == -1 and len(current_groups) < len(desired_groups):
        return False

    truncated_desired: List[int] = desired_groups[: len(current_groups)]

    # last digit might not be completely full
    # rest of prefix matches up
    if current_groups[:-1] == truncated_desired[:-1]:
        if current_groups[-1] == truncated_desired[-1]:
            return True
        elif current_groups[-1] < truncated_desired[-1]:
            # should only be less if last current group is not done yet
            if unknown_index != -1 and row[unknown_index - 1] == DAMAGED_SPRING:
                return True

    return False


def try_all_possible_combinations(row: List[str], desired_groups: List[int]) -> int:
    """let dp(i, j, k) = number of ways to fill in '?' in row for index i and onward,
    when every '?' has been filled to before index i, such that it matches desired_groups,
    and there are still j damaged springs to fill
    and row[i-1] is an undamaged spring (or i == 0) if k == 0, else row[i-1] is a damaged spring if k == 1
    """
    logger.info(f"\n{row=} and {desired_groups=}")
    num_damaged_springs_left: int = sum(desired_groups) - len(
        [i for i, v in enumerate(row) if v == DAMAGED_SPRING]
    )

    # store results from recursion: store dp(i, j, k)
    cache: List[List[List[Optional[int]]]] = [
        [[None] * 2 for i in range(1 + num_damaged_springs_left)]
        for j in range(len(row))
    ]

    def fill_in_one_position(
        row: List[str],
        row_index: int,
        num_damaged_springs_left: int,
        cache: List[List[List[Optional[int]]]],
    ) -> int:
        """Recursive function that finds how many ways to fill in row from row_index onwards by changing the remaining
        '?' blocks to '#' or '.' such that it fits desired_groups.
        """
        global num_times_called_recursive_function
        num_times_called_recursive_function += 1

        if num_damaged_springs_left < 0:
            return 0
        if row_index == len(row):
            if (
                num_damaged_springs_left == 0
                and group_up_completed(row) == desired_groups
            ):
                return 1
            return 0

        # only fill in "?" blocks
        if row[row_index] != UNKNOWN:
            return fill_in_one_position(
                row, 1 + row_index, num_damaged_springs_left, cache
            )

        if (row_index == 0 or row[row_index - 1] == NORMAL_SPRING) and cache[row_index][
            num_damaged_springs_left
        ][0] is not None:
            return cache[row_index][num_damaged_springs_left][0]
        if (
            row_index > 0
            and row[row_index - 1] == DAMAGED_SPRING
            and cache[row_index][num_damaged_springs_left][1] is not None
        ):
            return cache[row_index][num_damaged_springs_left][1]

        answer: int = 0
        tmp1 = None
        tmp2 = None

        # try placing damaged spring
        row[row_index] = DAMAGED_SPRING
        if plausibly_works(row, desired_groups):
            tmp1 = fill_in_one_position(
                row, 1 + row_index, num_damaged_springs_left - 1, cache
            )
            answer += tmp1

        # try placing normal spring
        row[row_index] = NORMAL_SPRING
        if plausibly_works(row, desired_groups):
            tmp2 = fill_in_one_position(
                row, 1 + row_index, num_damaged_springs_left, cache
            )
            answer += tmp2

        row[row_index] = UNKNOWN

        #  cache[row_index][num_damaged_springs_left] = answer
        if row_index == 0 or row[row_index - 1] == NORMAL_SPRING:
            #  logger.info(f'Setting cache[{row_index}][{num_damaged_springs_left}][0] = {answer} = {tmp1} + {tmp2}')
            cache[row_index][num_damaged_springs_left][0] = answer
        if row_index > 0 and row[row_index - 1] == DAMAGED_SPRING:
            #  logger.info(f'Setting cache[{row_index}][{num_damaged_springs_left}][1] = {answer} = {tmp1} + {tmp2}')
            cache[row_index][num_damaged_springs_left][1] = answer

        return answer

    answer: int = fill_in_one_position(row, 0, num_damaged_springs_left, cache)

    return answer


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day12.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    answer: int = 0

    for index, line in enumerate(input_lines):
        logger.info(f"Starting computation of line #{1 + index}")
        parts: List[str] = line.split(" ")
        row = [s for s in "?".join([parts[0]] * INPUT_MULTIPLIER)]
        desired_groups: List[int] = [
            int(s) for s in parts[1].split(",")
        ] * INPUT_MULTIPLIER

        answer += try_all_possible_combinations(row, desired_groups)

    logger.info(f"{answer=}")  # 527570479489

    logger.info(f"{num_times_called_recursive_function=}")

    #  answer=527570479489
    #  num_times_called_recursive_function=820053

    # that is, 527,570,479,489


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
