import time
from typing import Dict, List, Tuple

from loguru import logger

DEBUG: bool = False


def gcd(a: int, b: int) -> int:
    return a if b == 0 else gcd(b, a % b)


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def simulate_one_path_until_z_node(
    start_node: str,
    node_children: Dict[str, Tuple[str, str]],
    lr_instructions: str,
    lr_instructions_index: int,
) -> Tuple[str, int]:
    """Starting at start_node at this instruction of L/R, keep walking until
    reaching a node that ends with "Z".

    Return (which node you ended at, how many steps you took).
    """
    num_steps: int = 0
    curr_node: str = start_node

    logger.debug(
        f"Calling simulate_one_path_until_z_node with {start_node=} and LR {lr_instructions_index}"
    )

    if curr_node.endswith("Z"):
        if lr_instructions[lr_instructions_index] == "L":
            curr_node = node_children[curr_node][0]
        else:
            curr_node = node_children[curr_node][1]

        num_steps += 1
        lr_instructions_index = (lr_instructions_index + 1) % len(lr_instructions)

    while not curr_node.endswith("Z"):
        if lr_instructions[lr_instructions_index] == "L":
            curr_node = node_children[curr_node][0]
        else:
            curr_node = node_children[curr_node][1]

        num_steps += 1
        lr_instructions_index = (lr_instructions_index + 1) % len(lr_instructions)

    return (curr_node, num_steps)


def calc_shortest_path(
    lr_instructions: str, triplets: List[Tuple[str, str, str]]
) -> int:
    # map from node to its left and right node
    node_children: Dict[str, Tuple[str, str]] = dict()
    for triple in triplets:
        node_children[triple[0]] = (triple[1], triple[2])

    start_nodes: List[str] = [
        triple[0] for triple in triplets if triple[0].endswith("A")
    ]

    answer: int = 1

    # the number of steps form a starting node to a Z node, is empirically observed to be the same
    # as the number of steps from that z node to its next z node.
    # So answer is just the lcm of all of these step sizes
    for curr_node in start_nodes:
        # move curr_node to next z node
        _, individual_journey_steps = simulate_one_path_until_z_node(
            curr_node, node_children, lr_instructions, 0
        )

        logger.debug(
            f"for start_node {curr_node}, use {individual_journey_steps} steps"
        )
        answer = lcm(answer, individual_journey_steps)

    return answer


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
    logger.info(f"{answer=}")  # 13740108158591

    # 13,740,108,158,591


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
