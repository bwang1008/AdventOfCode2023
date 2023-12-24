import time
from typing import Dict, List

from loguru import logger

DEBUG: bool = False

ROUND: str = "O"
SQUARE: str = "#"
EMPTY: str = "."

NUM_CYCLES: int = 1_000_000_000


def calc_north_load(board: List[List[str]]) -> int:
    R: int = len(board)
    C: int = len(board[0])

    answer: int = 0

    for col in range(C):
        round_final_positions: List[int] = []

        for row in range(R):
            if board[row][col] == ROUND:
                round_final_positions.append(row)

        # convert row positions into load weight
        answer += sum(R - row for row in round_final_positions)

    return answer


def tilt_north(board: List[List[str]]) -> List[List[str]]:
    R: int = len(board)
    C: int = len(board[0])

    for col in range(C):
        next_final_position: int = 0  # row of next round stone when rolled north

        for row in range(R):
            if board[row][col] == SQUARE:
                next_final_position = row + 1
            elif board[row][col] == ROUND:
                board[row][col] = EMPTY
                board[next_final_position][col] = ROUND
                next_final_position += 1

    return board


def tilt_south(board: List[List[str]]) -> List[List[str]]:
    R: int = len(board)
    C: int = len(board[0])

    for col in range(C):
        next_final_position: int = R - 1  # row of next round stone when rolled south

        for row in range(R - 1, -1, -1):
            if board[row][col] == SQUARE:
                next_final_position = row - 1
            elif board[row][col] == ROUND:
                board[row][col] = EMPTY
                board[next_final_position][col] = ROUND
                next_final_position -= 1

    return board


def tilt_west(board: List[List[str]]) -> List[List[str]]:
    R: int = len(board)
    C: int = len(board[0])

    for row in range(R):
        next_final_position: int = 0  # col of next round stone when rolled west

        for col in range(C):
            if board[row][col] == SQUARE:
                next_final_position = col + 1
            elif board[row][col] == ROUND:
                board[row][col] = EMPTY
                board[row][next_final_position] = ROUND
                next_final_position += 1

    return board


def tilt_east(board: List[List[str]]) -> List[List[str]]:
    R: int = len(board)
    C: int = len(board[0])

    for row in range(R):
        next_final_position: int = C - 1  # col of next round stone when rolled east

        for col in range(C - 1, -1, -1):
            if board[row][col] == SQUARE:
                next_final_position = col - 1
            elif board[row][col] == ROUND:
                board[row][col] = EMPTY
                board[row][next_final_position] = ROUND
                next_final_position -= 1

    return board


def spin_cycle(board: List[List[str]]) -> List[List[str]]:
    return tilt_east(tilt_south(tilt_west(tilt_north(board))))


def many_spin_cycles(board: List[List[str]], num_cycles: int) -> List[List[str]]:
    history: Dict[str, int] = {}

    def to_string(board: List[List[str]]) -> str:
        return "".join("".join(row) for row in board)

    def from_string(board_str: str, R: int, C: int) -> List[List[str]]:
        return [[board_str[row * C + col] for col in range(C)] for row in range(R)]

    for iteration in range(1, num_cycles + 1):
        if iteration % 10000 == 0:
            logger.debug(f"{iteration=}")

        board = spin_cycle(board)

        board_str = to_string(board)
        if board_str in history:
            logger.info(
                f"Got a duplicate at iteration {iteration} at previous iteration {history[board_str]}"
            )

            cycle_len: int = iteration - history[board_str]
            # board already made first step again in the cycle, so roll back to last one
            remaining_iterations: int = (
                num_cycles - iteration - 1 + cycle_len
            ) % cycle_len
            last_cycle_index_in_history: int = history[board_str] + remaining_iterations

            logger.debug(
                f"Cycle length = {cycle_len} with remaining_iterations = {remaining_iterations} and last_cycle_index_in_history = {last_cycle_index_in_history}"
            )

            return from_string(
                list(history.keys())[last_cycle_index_in_history],
                len(board),
                len(board[0]),
            )

        else:
            history[board_str] = iteration

    return board


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day14.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    board: List[List[str]] = [[s for s in line] for line in input_lines]

    board = many_spin_cycles(board, NUM_CYCLES)

    answer: int = calc_north_load(board)
    logger.info(f"{answer=}")  # 104409


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
