import time
from queue import Queue
from typing import Dict, List, Tuple

from loguru import logger

DEBUG: bool = False


def is_valid(row: int, col: int, R: int, C: int) -> bool:
    return 0 <= row < R and 0 <= col < C


def get_neighbor_list(node_position: Tuple[int, int]) -> List[Tuple[int, int]]:
    row: int = node_position[0]
    col: int = node_position[1]
    dxs: List[int] = [-1, 0, 1, 0]
    dys: List[int] = [0, 1, 0, -1]

    return [(row + dxs[k], col + dys[k]) for k in range(len(dxs))]


def create_index_of_intersections(board: List[List[str]]) -> Dict[Tuple[int, int], int]:
    answer: Dict[Tuple[int, int], int] = {}

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "I":
                answer[(i, j)] = len(answer)

    return answer


def generate_graph(board: List[List[str]]) -> Dict[int, List[Tuple[int, int]]]:
    """Create edge list: a map from intersection-index to List(intersection-index neighbor, distance to neighbor)"""
    R: int = len(board)
    C: int = len(board[0])

    intersection_position_to_index: Dict[
        Tuple[int, int], int
    ] = create_index_of_intersections(board)
    intersection_index_to_position: List[Tuple[int, int]] = [
        k for k in intersection_position_to_index
    ]

    logger.info(f"{intersection_position_to_index=}")

    N: int = len(intersection_position_to_index)

    edges: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(N)}

    # bfs on each node
    for start_node in range(N):
        start_node_position: Tuple[int, int] = intersection_index_to_position[
            start_node
        ]
        q: Queue = Queue()
        q.put(start_node_position)

        visited: List[List[bool]] = [[False] * C for i in range(R)]
        distance: List[List[int]] = [[R * C + 1] * C for i in range(R)]

        distance[start_node_position[0]][start_node_position[1]] = 0

        while not q.empty():
            node_position: Tuple[int, int] = q.get()

            if visited[node_position[0]][node_position[1]]:
                continue
            visited[node_position[0]][node_position[1]] = True

            for neighbor_position in get_neighbor_list(node_position):
                if (
                    is_valid(neighbor_position[0], neighbor_position[1], R, C)
                    and not visited[neighbor_position[0]][neighbor_position[1]]
                ):
                    row2: int = neighbor_position[0]
                    col2: int = neighbor_position[1]

                    if board[row2][col2] == "I":
                        distance[row2][col2] = min(
                            1 + distance[node_position[0]][node_position[1]],
                            distance[row2][col2],
                        )
                        neighbor_intersection_index: int = (
                            intersection_position_to_index[neighbor_position]
                        )
                        edges[start_node].append(
                            (neighbor_intersection_index, distance[row2][col2])
                        )
                    elif board[row2][col2] == ".":
                        distance[row2][col2] = min(
                            1 + distance[node_position[0]][node_position[1]],
                            distance[row2][col2],
                        )
                        q.put((row2, col2))

    return edges


def dfs(edges: Dict[int, List[Tuple[int, int]]]) -> int:
    N: int = len(edges)
    visited: List[bool] = [False] * N

    def dfs_helper(node: int, current_dist_traveled: int, history: List[int]) -> int:
        if node == N - 1:
            logger.debug(f"Path length {current_dist_traveled} of history {history}")
            return current_dist_traveled

        if visited[node]:
            return -1

        visited[node] = True
        history.append(node)

        answer: int = 0
        for neighbor, edge_dist in edges[node]:
            if not visited[neighbor]:
                candidate_answer: int = dfs_helper(
                    neighbor, current_dist_traveled + edge_dist, history
                )
                answer = max(candidate_answer, answer)

        visited[node] = False
        del history[-1]

        return answer

    return dfs_helper(0, 0, [])


def transform_board(board: List[List[str]]) -> None:
    # clear out arrows
    R: int = len(board)
    C: int = len(board[0])

    for i in range(R):
        for j in range(C):
            if board[i][j] in {">", "^", "<", "v"}:
                board[i][j] = "."

    # find intersection nodes: those that have at least 3 dots surroudning it
    for i in range(C):
        for j in range(C):
            if board[i][j] == ".":
                num_path_neighbors: int = 0
                for row2, col2 in get_neighbor_list((i, j)):
                    if is_valid(row2, col2, R, C) and board[row2][col2] == ".":
                        num_path_neighbors += 1

                if num_path_neighbors >= 3:
                    board[i][j] = "I"

    # mark begin and end nodes as intersection nodes
    board[0][1] = "I"
    board[R - 1][C - 2] = "I"


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day23.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    board: List[List[str]] = [list(line) for line in input_lines]
    transform_board(board)

    edges: Dict[int, List[Tuple[int, int]]] = generate_graph(board)

    answer: int = dfs(edges)
    logger.info(f"{answer=}")  # 6434

    logger.debug(f"{edges=}")

    intersection_position_to_index: Dict[
        Tuple[int, int], int
    ] = create_index_of_intersections(board)
    intersection_index_to_position: List[Tuple[int, int]] = [
        k for k in intersection_position_to_index
    ]

    from pprint import pprint

    pprint(intersection_index_to_position)
    logger.info(f'There are {len(edges)} nodes')

    #  pprint(input_lines)

    # There are 36 nodes
    # Took 277s 28.896ms


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
