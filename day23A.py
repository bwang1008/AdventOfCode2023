import time
from queue import Queue
from typing import Dict, List, Tuple

from loguru import logger

DEBUG: bool = False

ARROWS: Dict[str, Tuple[int, int]] = {
    ">": (0, 1),
    "^": (-1, 0),
    "<": (0, -1),
    "v": (1, 0),
}


def is_valid(row: int, col: int, R: int, C: int) -> bool:
    return 0 <= row < R and 0 <= col < C


def get_neighbor_list(
    board: List[List[str]], node_position: Tuple[int, int]
) -> List[Tuple[int, int]]:
    row: int = node_position[0]
    col: int = node_position[1]
    dxs: List[int] = [-1, 0, 1, 0]
    dys: List[int] = [0, 1, 0, -1]

    if board[row][col] in ARROWS:
        changes: Tuple[int, int] = ARROWS[board[row][col]]
        return [(row + changes[0], col + changes[1])]

    return [(row + dxs[k], col + dys[k]) for k in range(len(dxs))]


def can_reach_arrow(
    board: List[List[str]], pos: Tuple[int, int], arrow: Tuple[int, int]
) -> bool:
    if board[arrow[0]][arrow[1]] == ">":
        return arrow[0] == pos[0] and arrow[1] == pos[1] + 1
    if board[arrow[0]][arrow[1]] == "^":
        return arrow[0] == pos[0] - 1 and arrow[1] == pos[1]
    if board[arrow[0]][arrow[1]] == "<":
        return arrow[0] == pos[0] and arrow[1] == pos[1] - 1
    if board[arrow[0]][arrow[1]] == "v":
        return arrow[0] == pos[0] + 1 and arrow[1] == pos[1]

    return False


def create_index_of_arrows(board: List[List[str]]) -> Dict[Tuple[int, int], int]:
    answer: Dict[Tuple[int, int], int] = {}

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] in ARROWS:
                answer[(i, j)] = len(answer)

    return answer


def generate_graph(board: List[List[str]]) -> Dict[int, List[Tuple[int, int]]]:
    """Create edge list: a map from arrow-index to List(arrow-index neighbor, distance to neighbor)"""
    R: int = len(board)
    C: int = len(board[0])

    # first mark start and end points
    board[0][1] = "v"
    board[R - 1][C - 2] = "v"

    arrow_position_to_index: Dict[Tuple[int, int], int] = create_index_of_arrows(board)
    arrow_index_to_position: List[Tuple[int, int]] = [
        k for k in arrow_position_to_index
    ]

    logger.info(f"{arrow_position_to_index=}")

    N: int = len(arrow_position_to_index)

    edges: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(N)}

    # bfs on each node
    for start_node in range(N):
        start_node_position: Tuple[int, int] = arrow_index_to_position[start_node]
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

            for neighbor_position in get_neighbor_list(board, node_position):
                if (
                    is_valid(neighbor_position[0], neighbor_position[1], R, C)
                    and not visited[neighbor_position[0]][neighbor_position[1]]
                ):
                    row2: int = neighbor_position[0]
                    col2: int = neighbor_position[1]

                    if board[row2][col2] in ARROWS and can_reach_arrow(
                        board, node_position, neighbor_position
                    ):
                        distance[row2][col2] = min(
                            1 + distance[node_position[0]][node_position[1]],
                            distance[row2][col2],
                        )
                        neighbor_arrow_index: int = arrow_position_to_index[
                            neighbor_position
                        ]

                        edges[start_node].append(
                            (neighbor_arrow_index, distance[row2][col2])
                        )
                        #  edges[neighbor_arrow_index].append(start_node)

                    elif board[row2][col2] == ".":
                        distance[row2][col2] = min(
                            1 + distance[node_position[0]][node_position[1]],
                            distance[row2][col2],
                        )
                        q.put((row2, col2))

    return edges


def topological_sort(edges: Dict[int, List[Tuple[int, int]]]) -> List[int]:
    def topological_sort_helper(node: int, visited: List[bool], stack: List[int]):
        visited[node] = True
        for neighbor, dist in edges[node]:
            if not visited[neighbor]:
                topological_sort_helper(neighbor, visited, stack)

        stack.append(node)

    N: int = len(edges)
    visited: List[bool] = [False] * N
    answer: List[int] = []

    for node in range(len(edges)):
        if not visited[node]:
            topological_sort_helper(node, visited, answer)

    answer.reverse()

    return answer


def longest_path_length_in_dag(edges: Dict[int, List[Tuple[int, int]]]) -> int:
    N: int = len(edges)

    topological_ordering: List[int] = topological_sort(edges)
    distances: List[int] = [0] * N

    logger.info(f"{topological_ordering=}")

    for node in topological_ordering:
        for neighbor, edge_dist in edges[node]:
            if distances[neighbor] < distances[node] + edge_dist:
                distances[neighbor] = distances[node] + edge_dist

    logger.info(f"{distances=}")

    return distances[-1]


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day23.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    board: List[List[str]] = [list(line) for line in input_lines]
    edges: Dict[int, List[Tuple[int, int]]] = generate_graph(board)

    answer: int = longest_path_length_in_dag(edges)
    logger.info(f"{answer=}")  # 1998


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
