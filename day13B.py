import time
from typing import List, Set, Tuple

from loguru import logger

DEBUG: bool = False


def transpose(board: List[List[str]]) -> List[List[str]]:
    return [
        [board[row][col] for row in range(len(board))] for col in range(len(board[0]))
    ]


def find_horizontal_reflections(board: List[List[str]]) -> List[int]:
    answer: Set[int] = set()
    R: int = len(board)

    def is_valid_horizontal_reflection(
        board: List[List[str]], reflection_row: int, changed: Tuple[int, int]
    ) -> bool:
        sum_of_rows: int = 2 * reflection_row - 1

        for row in range(R):
            row2: int = sum_of_rows - row

            if 0 <= row2 < R:
                if board[row] != board[row2]:
                    return False

        # there has to be a smudge on the mirror; so smudge has to be reflected / have
        # a valid row to reflect to
        changed_row: int = changed[0]
        if not 0 <= sum_of_rows - changed_row < R:
            return False

        return True

    for row in range(R):
        for col in range(len(board[row])):
            old_char: str = board[row][col]
            board[row][col] = "#" if old_char == "." else "."

            for i in range(1, R):
                if is_valid_horizontal_reflection(board, i, (row, col)):
                    logger.debug(
                        f"By switching board[{row}][{col}] from {old_char} to {board[row][col]}, got reflection at row {i}"
                    )

                    answer.add(i)

            board[row][col] = old_char

    return list(answer)


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

    logger.info(f"{answer=}")  # 32069


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
