from typing import List

from loguru import logger

DEBUG = False

def get_num_matches(winners: List[int], current_card: List[int]):
    num_matches = 0
    winner_set = set(winners)

    for num in current_card:
        if num in winner_set:
            num_matches += 1

    return num_matches


def calc_total_scratchcards(all_winners, all_current):
    N = len(all_current)

    num_cards = [1] * N

    for i in range(N):
        num_matches = get_num_matches(all_winners[i], all_current[i])

        for j in range(num_matches):
            num_cards[i + j + 1] += num_cards[i]

    return sum(num_cards)


def main():
    input_file = 'inputs/day04.txt'

    if DEBUG:
        input_file = 'inputs/dummy.txt'

    input_lines = []
    with open(input_file, 'r') as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    all_winners: List[List[int]] = []
    all_current: List[List[int]] = []

    for line in input_lines:
        numbers = line.split(': ')[1]

        winners, current = numbers.split(' | ')

        logger.debug(f'{winners=}')
        logger.debug(f'{current=}')

        winner_list = [int(s) for s in winners.split(' ') if s != '']
        current_list = [int(s) for s in current.split(' ') if s != '']

        all_winners.append(winner_list)
        all_current.append(current_list)

    answer = calc_total_scratchcards(all_winners, all_current)
    logger.info(f'{answer=}')  # 14427616


if __name__ == '__main__':
    main()
