import time
from typing import List

from loguru import logger

DEBUG = False


def all_zero(seq: List[int]) -> bool:
    return all(x == 0 for x in seq)


def calc_prev(seq: List[int]) -> int:
    seq.reverse()
    all_diffs: List[List[int]] = [seq]

    while not all_zero(all_diffs[-1]):
        next_diff: List[int] = []
        for i in range(1, len(all_diffs[-1])):
            next_diff.append(all_diffs[-1][i] - all_diffs[-1][i - 1])

        all_diffs.append(next_diff)

    prev_value: int = 0
    for seq_index in range(len(all_diffs) - 1, -1, -1):
        next_value: int = prev_value + all_diffs[seq_index][-1]
        all_diffs[seq_index].append(next_value)
        prev_value = next_value

    return all_diffs[0][-1]


def main() -> None:
    input_file = "inputs/day09.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    answer: int = 0
    for line in input_lines:
        answer += calc_prev([int(s) for s in line.split(" ")])

    logger.info(f"{answer=}")  # 1129


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
