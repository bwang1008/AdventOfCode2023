import time
import queue
from typing import Dict, List, Tuple

from loguru import logger

DEBUG: bool = False

RIGHT: int = 0
DOWN: int = 1
LEFT: int = 2
UP: int = 3

UPPER_RIGHT_REFLECT: Dict[int, int] = {
    RIGHT: UP,
    DOWN: LEFT,
    LEFT: DOWN,
    UP: RIGHT,
}

UPPER_LEFT_REFLECT: Dict[int, int] = {
    RIGHT: DOWN,
    DOWN: RIGHT,
    LEFT: UP,
    UP: LEFT,
}

EMPTY: str = "."
MIRROR_UPPER_RIGHT = "/"
MIRROR_UPPER_LEFT = "\\"
VERTICAL_SPLITTER = "|"
HORIZONTAL_SPLITTER = "-"


def valid(row: int, col: int, R: int, C: int) -> bool:
    return 0 <= row < R and 0 <= col < C


def get_neighbors(
    row: int, col: int, current_char: str, current_direction: int, R: int, C: int
) -> List[Tuple[int, int, int]]:
    potential_neighbors: List[Tuple[int, int, int]] = []

    right_neighbor: Tuple[int, int, int] = (row, col + 1, RIGHT)
    down_neighbor: Tuple[int, int, int] = (row + 1, col, DOWN)
    left_neighbor: Tuple[int, int, int] = (row, col - 1, LEFT)
    up_neighbor: Tuple[int, int, int] = (row - 1, col, UP)

    directional_neighbors: List[Tuple[int, int, int]] = [
        right_neighbor,
        down_neighbor,
        left_neighbor,
        up_neighbor,
    ]

    if current_char == EMPTY:
        potential_neighbors.append(directional_neighbors[current_direction])
    elif current_char == MIRROR_UPPER_RIGHT:
        reflected_direction: int = UPPER_RIGHT_REFLECT[current_direction]
        potential_neighbors.append(directional_neighbors[reflected_direction])
    elif current_char == MIRROR_UPPER_LEFT:
        reflected_direction = UPPER_LEFT_REFLECT[current_direction]
        potential_neighbors.append(directional_neighbors[reflected_direction])
    elif current_char == HORIZONTAL_SPLITTER:
        if current_direction in (LEFT, RIGHT):
            potential_neighbors.append(directional_neighbors[current_direction])
        else:
            potential_neighbors.append(directional_neighbors[LEFT])
            potential_neighbors.append(directional_neighbors[RIGHT])
    elif current_char == VERTICAL_SPLITTER:
        if current_direction in (UP, DOWN):
            potential_neighbors.append(directional_neighbors[current_direction])
        else:
            potential_neighbors.append(directional_neighbors[UP])
            potential_neighbors.append(directional_neighbors[DOWN])

    #  logger.debug(f'For {row=}, {col=} (a {current_char}), {current_direction=}, {potential_neighbors=}')

    return [
        neighbor
        for neighbor in potential_neighbors
        if valid(neighbor[0], neighbor[1], R, C)
    ]


def flood_fill(board: List[List[str]]) -> int:
    R: int = len(board)
    C: int = len(board[0])

    start_row: int = 0
    start_col: int = 0

    q: queue.Queue = queue.Queue()
    q.put((start_row, start_col, 0))

    visited: List[List[List[bool]]] = [
        [[False] * 4 for i in range(C)] for j in range(R)
    ]

    while not q.empty():
        row, col, direction = q.get()

        if visited[row][col][direction]:
            continue
        visited[row][col][direction] = True

        #  logger.debug(f'Checking out {row=},{col=} in direction {direction}')

        for neighbor in get_neighbors(row, col, board[row][col], direction, R, C):
            if not visited[neighbor[0]][neighbor[1]][neighbor[2]]:
                q.put(neighbor)

    count_visited: int = 0
    for row in visited:
        for col in row:
            if any(col):
                count_visited += 1

    return count_visited


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day16.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    board: List[List[str]] = [[s for s in line] for line in input_lines]

    answer: int = flood_fill(board)
    logger.info(f"{answer=}")  # 7517


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
