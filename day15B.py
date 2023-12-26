import time
from typing import Dict, List

from loguru import logger

DEBUG: bool = False

NUM_BOXES: int = 256


def calc_HASH(input_str: str) -> int:
    answer: int = 0
    for c in input_str:
        if c == "\n":
            continue
        answer += ord(c)
        answer = (17 * answer) % 256

    return answer


def calc_focusing_power(boxes: List[Dict[str, int]]) -> int:
    answer: int = 0

    for box_index, box in enumerate(boxes):
        for lens_index, lens_name in enumerate(box):
            answer += (1 + box_index) * (1 + lens_index) * box[lens_name]

    return answer


def run_commands(commands: List[str]) -> int:
    boxes: List[Dict[str, int]] = [{} for i in range(NUM_BOXES)]

    for command in commands:
        if command[-1] == "-":
            lens_name: str = command[:-1]

            box_index: int = calc_HASH(lens_name)
            if lens_name in boxes[box_index]:
                del boxes[box_index][lens_name]
        else:
            command_parts: List[str] = command.split("=", 1)
            lens_name = command_parts[0]
            focal_length: int = int(command_parts[1])

            box_index = calc_HASH(lens_name)
            boxes[box_index][lens_name] = focal_length

    return calc_focusing_power(boxes)


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day15.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    commands = input_lines[0].split(",")

    answer: int = run_commands(commands)
    logger.info(f"{answer=}")  # 267372


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
