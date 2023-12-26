import functools
import time
from queue import PriorityQueue
from typing import Dict, List, Tuple

from loguru import logger

DEBUG: bool = False

RIGHT: int = 0
UP: int = 1
LEFT: int = 2
DOWN: int = 3


@functools.total_ordering
class Node:
    def __init__(self, row: int, col: int, direction: int, num_same_direction: int):
        # (row, column, direction, how many times stepped in the direction)
        self.row: int = row
        self.col: int = col
        self.direction: int = direction
        self.num_same_direction: int = num_same_direction

    def __lt__(self, other) -> bool:
        return other.num_same_direction - self.num_same_direction

    def __eq__(self, other) -> bool:
        return self.num_same_direction == other.num_same_direction

    def __str__(self) -> str:
        what = {UP: "UP", DOWN: "DOWN", LEFT: "LEFT", RIGHT: "RIGHT"}
        return f"Node({self.row}, {self.col}, {what[self.direction]}, {self.num_same_direction})"

    def __hash__(self) -> int:
        return hash((self.row, self.col, self.direction, self.num_same_direction))


def valid(row: int, col: int, R: int, C: int) -> bool:
    return 0 <= row < R and 0 <= col < C


def get_neighbors(curr_node: Node) -> List[Node]:
    dxs: List[int] = [-1, 0, 1, 0]
    dys: List[int] = [0, 1, 0, -1]
    neighbor_directions: List[int] = [UP, RIGHT, DOWN, LEFT]

    potential_neighbors: List[Node] = []

    for dx, dy, neighbor_direction in zip(dxs, dys, neighbor_directions):
        row2: int = curr_node.row + dx
        col2: int = curr_node.col + dy

        potential_neighbors.append(
            Node(
                row2,
                col2,
                neighbor_direction,
                1
                if neighbor_direction != curr_node.direction
                else 1 + curr_node.num_same_direction,
            )
        )

    return [
        neighbor
        for neighbor in potential_neighbors
        if neighbor.num_same_direction <= 10
        # if move in different direction, must have had 4
        and (
            neighbor.direction == curr_node.direction
            or curr_node.num_same_direction >= 4
        )
        and abs(neighbor.direction - curr_node.direction) != 2
    ]


def dijkstra(
    heat_loss: List[List[int]],
    source: Tuple[int, int],
    dest: Tuple[int, int],
    initial_direction: int,
) -> int:
    R: int = len(heat_loss)
    C: int = len(heat_loss[0])

    BIG: int = 9 * R * C + 1

    visited: Dict[Node, bool] = {}
    dist: Dict[Node, int] = {}
    parents: Dict[Node, Node] = {}

    begin_node: Node = Node(source[0], source[1], initial_direction, 0)
    dist[begin_node] = 0

    pq: PriorityQueue = PriorityQueue()
    pq.put((0, begin_node))

    dest_row: int = dest[0]
    dest_col: int = dest[1]

    last_node: Node = Node(0, 0, 0, 0)

    while not pq.empty():
        old, curr_node = pq.get()

        #  logger.debug(f'Process {curr_node} with weight {old}')

        if curr_node in visited:
            continue
        visited[curr_node] = True

        if (
            curr_node.row == dest_row
            and curr_node.col == dest_col
            and curr_node.num_same_direction >= 4
        ):
            last_node = curr_node
            break

        for neighbor in get_neighbors(curr_node):
            if valid(neighbor.row, neighbor.col, R, C) and neighbor not in visited:
                new_dist: int = dist[curr_node] + heat_loss[neighbor.row][neighbor.col]

                #  logger.debug(f'Consider neighbor {neighbor} with {new_dist=}')

                if neighbor not in dist or new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    parents[neighbor] = curr_node
                    pq.put(
                        (
                            new_dist,
                            Node(
                                neighbor.row,
                                neighbor.col,
                                neighbor.direction,
                                neighbor.num_same_direction,
                            ),
                        )
                    )

    trail = [[False] * C for row in range(R)]
    curr = last_node
    while curr in parents:
        trail[curr.row][curr.col] = True
        curr = parents[curr]

    logger.debug("trail")
    for row in trail:
        for col in row:
            if col:
                print("X", end="")
            else:
                print(".", end="")
        print()

    answer: int = BIG
    for direction in range(4):
        for num_times in range(4, 10):
            last_node = Node(dest_row, dest_col, direction, num_times)
            answer = min(answer, dist.get(last_node, answer))

    logger.info(f"For {initial_direction=}, have {answer=}")
    return answer


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day17.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    heat_loss: List[List[int]] = [[int(s) for s in line] for line in input_lines]

    answer_right: int = dijkstra(
        heat_loss, (0, 0), (len(heat_loss) - 1, len(heat_loss[0]) - 1), RIGHT
    )
    answer_down: int = dijkstra(
        heat_loss, (0, 0), (len(heat_loss) - 1, len(heat_loss[0]) - 1), DOWN
    )
    answer: int = min(answer_right, answer_down)
    logger.info(f"{answer=}")  # 1382


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
