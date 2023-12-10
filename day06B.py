import math
import time
from typing import List

from loguru import logger

DEBUG: bool = False


def calc_num_ways_to_win_race(time: int, best_distance: int) -> int:
    # find number of x satisfy 0 <= x <= time and x * (time - x) > best_distance. Well best_distance > 0 so first condition is implied by second.
    # x^2 - time * x + best_distance < 0
    # r1 <= x <= r2 where r1, r2 = (time +- sqrt(time^2 - 4*best_distance)) / 2

    r1: int = int(math.ceil((time - math.sqrt(time**2 - 4 * best_distance)) / 2))
    r2: int = int(math.floor((time + math.sqrt(time**2 - 4 * best_distance)) / 2))

    logger.debug(f"{r1=} {r2=}")

    return r2 - r1 + 1


def main() -> None:
    input_file: str = "inputs/day06.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    time = int(input_lines[0][len("Time:") :].replace(" ", ""))
    distance = int(input_lines[1][len("Distance:") :].replace(" ", ""))

    logger.debug(f"{time=} {distance=}")

    answer: int = calc_num_ways_to_win_race(time, distance)

    logger.info(f"{answer=}")  # 28101347


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
