from typing import List, Set

from loguru import logger

DEBUG: bool = False


def get_num_matches(winners: List[int], current_card: List[int]) -> int:
    num_matches: int = 0
    winner_set: Set[int] = set(winners)

    for num in current_card:
        if num in winner_set:
            num_matches += 1

    return num_matches


def calc_total_scratchcards(
    all_winners: List[List[int]], all_current: List[List[int]]
) -> int:
    N: int = len(all_current)

    num_cards: List[int] = [1] * N

    for i in range(N):
        num_matches: int = get_num_matches(all_winners[i], all_current[i])

        for j in range(num_matches):
            num_cards[i + j + 1] += num_cards[i]

    return sum(num_cards)


def main() -> None:
    input_file: str = "inputs/day04.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    all_winners: List[List[int]] = []
    all_current: List[List[int]] = []

    for line in input_lines:
        numbers: str = line.split(": ")[1]

        winners, current = numbers.split(" | ")

        logger.debug(f"{winners=}")
        logger.debug(f"{current=}")

        winner_list: List[int] = [int(s) for s in winners.split(" ") if s != ""]
        current_list: List[int] = [int(s) for s in current.split(" ") if s != ""]

        all_winners.append(winner_list)
        all_current.append(current_list)

    answer: int = calc_total_scratchcards(all_winners, all_current)
    logger.info(f"{answer=}")  # 14427616


if __name__ == "__main__":
    main()
