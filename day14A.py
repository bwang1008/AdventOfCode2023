import time
from typing import List

from loguru import logger

DEBUG: bool = False

ROUND: str = "O"
SQUARE: str = "#"


def calc_north_load(board: List[List[str]]) -> int:
    R: int = len(board)
    C: int = len(board[0])

    answer: int = 0

    for col in range(C):
        round_final_positions: List[int] = []
        curr_position: int = 0  # location of next round stone when rolled north

        for row in range(R):
            if board[row][col] == ROUND:
                round_final_positions.append(curr_position)
                curr_position += 1
            elif board[row][col] == SQUARE:
                curr_position = row + 1

        # convert row positions into load weight
        answer += sum(R - row for row in round_final_positions)

    return answer


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day14.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    board: List[List[str]] = [[s for s in line] for line in input_lines]

    answer: int = calc_north_load(board)
    logger.info(f"{answer=}")  # 113486


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
