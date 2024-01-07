"""
Idea is to simulate the first several iterations, find the quadratic equation that fits,
and extrapolate to the desired number of steps.

Let N = the length of the board. The example given has N = 11; the input has N = 131.
We start with multiple copies of the board (say a 5 x 5 copies of the board) and
naively simulate with BFS. Keep track of the number of valid positions.

Suppose we have N = 11, we have a 55x55 expanded board, and simulated for 100 steps.
Suppose we desire step 2005. We look at steps[3], steps[14], steps[25], ... (multiples of N)
up til steps[91] (because our naive was for up to 10 steps. We look at the last few,
find that it can be desribed from a quadratic. Find the values of a, b, c so that
f(x) = a*x*x +bx + c, and extrapolate to find step 2005.

This script took 435s 789.311ms
"""

import time
from typing import List, Set, Tuple

from loguru import logger

DEBUG: bool = False

START_SYMBOL: str = "S"
GARDEN_PLOT: str = "."
ROCK: str = "#"

NAIVE_MULTIPLIER: int = 13


def expand_board(board: List[List[str]], k: int) -> List[List[str]]:
    R: int = len(board)
    C: int = len(board[0])

    return [[board[i % R][j % C] for i in range(C * k)] for j in range(R * k)]


def get_expanded_start_pos(
    start_pos: Tuple[int, int], R: int, C: int, k: int
) -> Tuple[int, int]:
    return (start_pos[0] + R * (k // 2), start_pos[1] + C * (k // 2))


def valid(board: List[List[str]], row: int, col: int) -> bool:
    return (
        0 <= row < len(board)
        and 0 <= col < len(board[row])
        and board[row][col] == GARDEN_PLOT
    )


def get_num_positions_n_away(
    board: List[List[str]], start_pos: Tuple[int, int], n: int
) -> List[int]:
    logger.info(f"Naive search for multiplier = {NAIVE_MULTIPLIER} and num_steps = {n}")
    zero_away: Set[Tuple[int, int]] = {start_pos}
    k_away = zero_away

    dx: List[int] = [-1, 0, 1, 0]
    dy: List[int] = [0, 1, 0, -1]

    history_count: List[int] = [1]

    for k in range(n):
        k_plus_1_away: Set[Tuple[int, int]] = set()

        if k % 10 == 0:
            logger.info(f"Naive process step {k}")

        for pos in k_away:
            for i in range(len(dx)):
                row2: int = pos[0] + dx[i]
                col2: int = pos[1] + dy[i]

                if valid(board, row2, col2):
                    k_plus_1_away.add((row2, col2))

        k_away = k_plus_1_away
        history_count.append(len(k_away))

    return history_count


def extrapolate(history_count: List[int], N: int, desired_step: int) -> int:
    # observed offline that count of visitable squares is eventually quadratic
    # get differences of differences, return that if consistent for past 3 runs.

    segmented_history_count: List[int] = history_count[(desired_step % N) :: N]
    diff_1 = [
        segmented_history_count[i] - segmented_history_count[i - 1]
        for i in range(1, len(segmented_history_count))
    ]
    diff_2 = [diff_1[i] - diff_1[i - 1] for i in range(1, len(diff_1))]

    found_index: int = -1
    diff_2_coefficient: int = -1
    for i in range(2, len(diff_2)):
        if diff_2[i - 2] == diff_2[i - 1] and diff_2[i - 1] == diff_2[i]:
            found_index = i
            diff_2_coefficient = diff_2[i]
            break

    if diff_2_coefficient == -1:
        logger.error(
            "No constant amount of diff_2 occurred. Consider using more naive history and a bigger naive grid"
        )
        return -1

    # y1 y2  y3
    #  da1 da2 (da2+c) (da2+2c) (da + 3c)
    #     c
    # add t*da2  + c * (t*(t+1)/2)

    logger.debug(f"{segmented_history_count[:found_index + 3]}")
    logger.debug(f"{diff_1[:found_index + 2]}")
    logger.debug(f"{diff_2[:found_index + 1]}")

    additional_num_function_steps: int = desired_step // N - (found_index + 2)
    prev_diff_1: int = diff_1[found_index + 1]
    to_add: int = (
        additional_num_function_steps * prev_diff_1
        + diff_2_coefficient
        * additional_num_function_steps
        * (additional_num_function_steps + 1)
        // 2
    )

    logger.debug(f"{additional_num_function_steps=}, {prev_diff_1=}, {to_add=}")
    logger.debug(f"Looking for steps at {desired_step}")

    return segmented_history_count[found_index + 2] + to_add


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day21.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    board: List[List[str]] = [[s for s in line] for line in input_lines]
    N: int = len(board)

    start_row: int = -1
    start_col: int = -1

    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if col == START_SYMBOL:
                start_row = row_index
                start_col = col_index
                board[start_row][start_col] = GARDEN_PLOT
                break

        if start_row != -1:
            break

    # manually set NAIVE_MULTIPLIER. Search naively until the borders: (NAIVE_MULTIPLIER // 2) * N (half the expanded border)
    history_count: List[int] = get_num_positions_n_away(
        expand_board(board, NAIVE_MULTIPLIER),
        get_expanded_start_pos(
            (start_row, start_col), len(board), len(board[0]), NAIVE_MULTIPLIER
        ),
        (NAIVE_MULTIPLIER // 2) * N,
    )

    # 26501365 was in the problem description
    answer: int = extrapolate(history_count, N, 26501365)
    logger.info(f"{answer=}")  # 636350496972143


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")


"""
2024-01-06 20:58:38.749 | DEBUG    | __main__:extrapolate:119 - [3943, 35126, 97407, 190786, 315263]
2024-01-06 20:58:38.749 | DEBUG    | __main__:extrapolate:120 - [31183, 62281, 93379, 124477]
2024-01-06 20:58:38.749 | DEBUG    | __main__:extrapolate:121 - [31098, 31098, 31098]
2024-01-06 20:58:38.749 | DEBUG    | __main__:extrapolate:127 - additional_num_function_steps=202296, prev_diff_1=124477, to_add=636350496656880
2024-01-06 20:58:38.749 | DEBUG    | __main__:extrapolate:128 - Looking for steps at 26501365
2024-01-06 20:58:38.750 | INFO     | __main__:main:162 - answer=636350496972143
"""
