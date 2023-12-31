import time
from typing import List, Set, Tuple

from loguru import logger

DEBUG: bool = False

START_SYMBOL: str = "S"
GARDEN_PLOT: str = "."
ROCK: str = "#"


def valid(board: List[List[str]], row: int, col: int) -> bool:
    return (
        0 <= row < len(board)
        and 0 <= col < len(board[row])
        and board[row][col] == GARDEN_PLOT
    )


def get_positions_n_away(
    board: List[List[str]], start_pos: Tuple[int, int], n: int
) -> Set[Tuple[int, int]]:
    zero_away: Set[Tuple[int, int]] = {start_pos}
    k_away = zero_away

    dx: List[int] = [-1, 0, 1, 0]
    dy: List[int] = [0, 1, 0, -1]

    for k in range(n):
        k_plus_1_away: Set[Tuple[int, int]] = set()

        for pos in k_away:
            for i in range(len(dx)):
                row2: int = pos[0] + dx[i]
                col2: int = pos[1] + dy[i]

                if valid(board, row2, col2):
                    k_plus_1_away.add((row2, col2))

        k_away = k_plus_1_away

        #  logger.debug(f'After {k + 1} steps, can get to {k_away}')

    return k_away


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day21.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    board: List[List[str]] = [[s for s in line] for line in input_lines]

    start_row: int = -1
    start_col: int = -1

    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if col == START_SYMBOL:
                start_row = row_index
                start_col = col_index
                board[start_row][start_col] = GARDEN_PLOT
                break

        if start_row != -1:
            break

    answer: int = len(get_positions_n_away(board, (start_row, start_col), 64))
    logger.info(f"{answer=}")  # 3858


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
