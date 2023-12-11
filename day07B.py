import time
from collections import Counter
from functools import cmp_to_key
from typing import List, Tuple

from loguru import logger

DEBUG: bool = False


def get_raw_hand_type(hand: str) -> int:
    char_counts: Counter = Counter(hand)

    if len(char_counts) == 5:
        # high card
        return 0
    elif len(char_counts) == 4:
        # one pair
        return 1
    elif len(char_counts) == 3:
        if 3 not in char_counts.values():
            # two pair
            return 2
        # three of a kind
        return 3
    elif len(char_counts) == 2:
        if 3 in char_counts.values():
            # full house
            return 4
        # four of a kind
        return 5

    # five of a kind
    return 6


def get_hand_type_while_interpreting_j(hand: str) -> int:
    def generate_all_candidates(hand: str) -> List[str]:
        """Interpret J as any character."""
        j_replacement: str = "23456789TQKA"

        def helper(
            chars: List[str], original_hand: str, accumulator: List[str]
        ) -> None:
            if len(chars) == 5:
                accumulator.append("".join(chars))
                return

            current_index: int = len(chars)

            if original_hand[current_index] != "J":
                chars.append(original_hand[current_index])
                helper(chars, original_hand, accumulator)
                chars.pop()
            else:
                for replacement_char in j_replacement:
                    chars.append(replacement_char)
                    helper(chars, original_hand, accumulator)
                    chars.pop()

        accumulator: List[str] = []
        helper([], hand, accumulator)

        return accumulator

    all_replacements = generate_all_candidates(hand)

    return max(
        get_raw_hand_type(hand_replacement) for hand_replacement in all_replacements
    )


def compare_number(a: str, b: str) -> int:
    alphabet = "J23456789TQKA"

    for i in range(len(a)):
        r1 = alphabet.find(a[i])
        r2 = alphabet.find(b[i])

        if r1 != r2:
            return r1 - r2

    return 0


def compare_hands(hand1: Tuple[str, int], hand2: Tuple[str, int]) -> int:
    hand_type_1 = get_hand_type_while_interpreting_j(hand1[0])
    hand_type_2 = get_hand_type_while_interpreting_j(hand2[0])

    #  logger.debug(f'hand_type of {hand1[0]} = {hand_type_1}')
    #  logger.debug(f'hand_type of {hand2[0]} = {hand_type_2}')

    if hand_type_1 == hand_type_2:
        return compare_number(hand1[0], hand2[0])

    return hand_type_1 - hand_type_2


def sorted_inputs(inputs: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    sorted_list = sorted(inputs, key=cmp_to_key(compare_hands))

    return sorted_list


def main() -> None:
    input_file: str = "inputs/day07.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    inputs: List[Tuple[str, int]] = []
    for line in input_lines:
        parts = line.split(" ")
        inputs.append((parts[0], int(parts[1])))

    sorted_list = sorted_inputs(inputs)

    logger.debug(f"{sorted_list=}")

    answer: int = 0
    for i, hand in enumerate(sorted_list):
        answer += (i + 1) * hand[1]

    logger.info(f"{answer=}")  # 251195607


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
