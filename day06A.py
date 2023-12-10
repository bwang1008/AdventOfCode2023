import time
from typing import List

from loguru import logger

DEBUG: bool = False


def calc_num_ways_to_win_race(time: int, best_distance: int) -> int:
    num_ways: int = 0
    for i in range(time + 1):
        time_pressing: int = i
        time_going: int = time - time_pressing

        distance: int = time_pressing * time_going

        if distance > best_distance:
            num_ways += 1

    return num_ways


def main() -> None:
    input_file: str = "inputs/day06.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    times: List[int] = [
        int(s) for s in input_lines[0][len("Time:") :].split(" ") if s != ""
    ]
    distances: List[int] = [
        int(s) for s in input_lines[1][len("Distance:") :].split(" ") if s != ""
    ]

    answer: int = 1
    for race in range(len(times)):
        answer *= calc_num_ways_to_win_race(times[race], distances[race])

    logger.info(f"{answer=}")  # 861300


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
