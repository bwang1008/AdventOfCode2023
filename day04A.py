from typing import List

from loguru import logger

DEBUG = False


def calc_score(winners: List[int], current_card: List[int]):
    current_score = 0

    winner_set = set(winners)

    for num in current_card:
        if num in winner_set:
            if current_score == 0:
                current_score = 1
            else:
                current_score *= 2

    return current_score


def main():
    input_file = "inputs/day04.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    answer = 0

    for line in input_lines:
        numbers = line.split(": ")[1]

        winners, current = numbers.split(" | ")

        logger.debug(f"{winners=}")
        logger.debug(f"{current=}")

        winner_list = [int(s) for s in winners.split(" ") if s != ""]
        current_list = [int(s) for s in current.split(" ") if s != ""]

        answer += calc_score(winner_list, current_list)

    logger.info(f"{answer=}")  # 25004


if __name__ == "__main__":
    main()
