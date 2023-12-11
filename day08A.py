import time
from typing import Dict, List, Tuple

from loguru import logger

DEBUG: bool = False


def calc_shortest_path(
    lr_instructions: str, triplets: List[Tuple[str, str, str]]
) -> int:
    node_children: Dict[str, Tuple[str, str]] = dict()
    for triple in triplets:
        node_children[triple[0]] = (triple[1], triple[2])

    steps_taken: int = 0

    start_node: str = "AAA"
    end_node: str = "ZZZ"

    curr_node: str = start_node
    lr_instructions_index: int = 0

    while curr_node != end_node:
        curr_node_children: Tuple[str, str] = node_children[curr_node]
        if lr_instructions[lr_instructions_index] == "L":
            curr_node = curr_node_children[0]
        else:
            curr_node = curr_node_children[1]

        steps_taken += 1
        lr_instructions_index = (lr_instructions_index + 1) % len(lr_instructions)

    return steps_taken


def main() -> None:
    input_file: str = "inputs/day08.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    lr_instructions: str = input_lines[0]

    triplets: List[Tuple[str, str, str]] = []
    for i in range(2, len(input_lines)):
        line = input_lines[i]
        # AAA = (BBB, CCC)
        # 0123456789012345
        triplets.append((line[0:3], line[7:10], line[12:15]))

    answer: int = calc_shortest_path(lr_instructions, triplets)
    logger.info(f"{answer=}")  # 11309


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
