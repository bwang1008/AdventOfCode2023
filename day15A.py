import time
from typing import List

from loguru import logger

DEBUG: bool = False


def calc_HASH(input_str: str) -> int:
    answer: int = 0
    for c in input_str:
        if c == "\n":
            continue
        answer += ord(c)
        answer = (17 * answer) % 256

    return answer


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day15.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    answer: int = sum(calc_HASH(input_str) for input_str in input_lines[0].split(","))
    logger.info(f"{answer=}")  # 517965


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
