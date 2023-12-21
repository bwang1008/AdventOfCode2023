import time
from typing import Dict, List, Tuple

from loguru import logger

DEBUG: bool = False

neighbor_map: Dict[str, List[Tuple[int, int]]] = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "F": [(0, 1), (1, 0)],
    "7": [(1, 0), (0, -1)],
    "J": [(0, -1), (-1, 0)],
}


def valid(row: int, col: int, R: int, C: int) -> bool:
    return 0 <= row < R and 0 <= col < C


def get_potential_neighbors(
    character: str, row: int, col: int
) -> List[Tuple[int, int]]:
    changes: List[Tuple[int, int]] = neighbor_map.get(character, [])
    return [(row + dx, col + dy) for dx, dy in changes]


def verify_connection(board: List[List[str]], start_row: int, start_col: int) -> bool:
    current: str = board[start_row][start_col]
    R: int = len(board)
    C: int = len(board)

    num_matching: int = 0

    # points up
    if (
        current in {"|", "L", "J"}
        and valid(start_row - 1, start_col, R, C)
        and board[start_row - 1][start_col] in {"|", "F", "7"}
    ):
        num_matching += 1
    # points right
    if (
        current in {"-", "L", "F"}
        and valid(start_row, start_col + 1, R, C)
        and board[start_row][start_col + 1] in {"-", "7", "J"}
    ):
        num_matching += 1
    # points left
    if (
        current in {"-", "7", "J"}
        and valid(start_row, start_col + 1, R, C)
        and board[start_row][start_col - 1] in {"-", "L", "F"}
    ):
        num_matching += 1
    # points down
    if (
        current in {"|", "F", "7"}
        and valid(start_row, start_col + 1, R, C)
        and board[start_row + 1][start_col] in {"|", "L", "J"}
    ):
        num_matching += 1

    return num_matching == 2


def dfs_distances(
    board: List[List[str]], start_row: int, start_col: int
) -> List[List[int]]:
    R: int = len(board)
    C: int = len(board[0])

    visited: List[List[bool]] = [[False] * C for row in range(R)]
    distances: List[List[int]] = [[R * C + 1] * C for row in range(R)]
    distances[start_row][start_col] = 0

    stack: List[Tuple[int, int]] = [(start_row, start_col)]

    while stack:
        curr_row, curr_col = stack.pop()

        if visited[curr_row][curr_col]:
            continue
        visited[curr_row][curr_col] = True

        for neighbor_row, neighbor_col in get_potential_neighbors(
            board[curr_row][curr_col], curr_row, curr_col
        ):
            if (
                valid(neighbor_row, neighbor_col, R, C)
                and board[neighbor_row][neighbor_col] != "."
                and not visited[neighbor_row][neighbor_col]
            ):
                distances[neighbor_row][neighbor_col] = min(
                    distances[neighbor_row][neighbor_col],
                    1 + distances[curr_row][curr_col],
                )

                stack.append((neighbor_row, neighbor_col))

                # limit to one neighbor added / searched (for beginning node)
                break

    # fill rest of distances with -1
    for row in range(R):
        for col in range(C):
            if distances[row][col] == R * C + 1:
                distances[row][col] = -1

    return distances


def find_loop_inner_area(board: List[List[str]], start_row: int, start_col: int) -> int:
    for s in neighbor_map:
        board[start_row][start_col] = s
        logger.debug(f"Try using {s=}")

        if not verify_connection(board, start_row, start_col):
            logger.info(
                f"Skipping connection {s} because does not connect with 2 neighbors"
            )
            continue

        break

    distances: List[List[int]] = dfs_distances(board, start_row, start_col)

    area: int = 0

    # determine the actual area of the interior:
    # using each upper-left corner to determine if square is interior or exterior
    for row in range(len(distances) - 1):
        # outer-most border is always exterior
        inside: bool = False

        for col in range(len(distances[row]) - 1):
            if distances[row][col] > -1:
                curr: str = board[row][col]

                # toggle if square is inside or outside by determining
                # if top-left corner points down
                if curr in {"|", "7", "F"}:
                    inside = not inside
            if inside:
                #  logger.debug(f'Adding area on {row=}, {col=}')
                area += 1

    logger.info(f"{area=}")

    # get length of border
    border_length: int = 0
    for neighbor_row, neighbor_col in get_potential_neighbors(
        board[start_row][start_col], start_row, start_col
    ):
        if (
            valid(neighbor_row, neighbor_col, len(board), len(board[0]))
            and board[neighbor_row][neighbor_col] != "."
        ):
            border_length = max(
                border_length, 1 + distances[neighbor_row][neighbor_col]
            )

    logger.info(f"{border_length=}")

    # Pick's Theorem
    return area + 1 - (border_length // 2)


def main() -> None:
    input_file: str = "inputs/day10.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    board: List[List[str]] = [[c for c in line] for line in input_lines]

    start_row: int = -1
    start_col: int = -1

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "S":
                start_row = i
                start_col = j
                break

        if start_row != -1:
            break

    answer: int = find_loop_inner_area(board, start_row, start_col)

    logger.info(f"{answer=}")  # 415


if __name__ == "__main__":
    start_time = time.time()
    main()

    logger.info(f"Took {time.time() - start_time}")
