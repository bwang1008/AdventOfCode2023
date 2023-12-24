import time
from typing import List

from loguru import logger

DEBUG: bool = False


def transpose(board: List[List[str]]) -> List[List[str]]:
    return [
        [board[row][col] for row in range(len(board))] for col in range(len(board[0]))
    ]


def find_horizontal_reflections(board: List[List[str]]) -> List[int]:
    answer: List[int] = []
    R: int = len(board)

    for i in range(1, R):
        valid_reflection = True
        sum_of_rows: int = 2 * i - 1

        for row in range(R):
            row2: int = sum_of_rows - row

            if 0 <= row2 < R:
                if board[row] != board[row2]:
                    valid_reflection = False
                    break

        if valid_reflection:
            answer.append(i)

    return answer


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day13.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    boards: List[List[List[str]]] = []

    current_board: List[List[str]] = []
    for line in input_lines:
        if line == "":
            boards.append(current_board)
            current_board = []
        else:
            current_board.append([s for s in line])

    boards.append(current_board)

    horizontal_reflections: List[List[int]] = [
        find_horizontal_reflections(board) for board in boards
    ]
    vertical_reflections: List[List[int]] = [
        find_horizontal_reflections(transpose(board)) for board in boards
    ]

    answer: int = 100 * sum([sum(indv) for indv in horizontal_reflections]) + sum(
        [sum(indv) for indv in vertical_reflections]
    )

    logger.info(f"{answer=}")  # 39939


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
