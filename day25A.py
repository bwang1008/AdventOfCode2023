import time
from pprint import pprint
from queue import Queue
from typing import Dict, List, Set, Tuple

from loguru import logger

DEBUG: bool = False


def bfs(edges: List[List[int]], source: int, sink: int, ret: str = "path") -> List[int]:
    N: int = len(edges)

    visited: List[bool] = [False] * N
    parent: List[int] = [-1] * N
    distances: List[int] = [N**3] * N

    distances[source] = 0

    q: Queue = Queue()
    q.put(source)

    while not q.empty():
        curr: int = q.get()
        if curr == sink:
            break

        if visited[curr]:
            continue
        visited[curr] = True

        for neighbor in range(N):
            if not visited[neighbor] and edges[curr][neighbor] > 0:
                parent[neighbor] = curr
                distances[neighbor] = min(
                    distances[neighbor], distances[curr] + edges[curr][neighbor]
                )
                q.put(neighbor)

    if ret == "dist":
        for i in range(N):
            if distances[i] == N**3:
                distances[i] = -1
        return distances

    if ret == "parent":
        return parent

    path: List[int] = []
    if parent[sink] == -1:
        return path

    curr = sink
    while curr != -1:
        path.append(curr)
        curr = parent[curr]

    return path


def max_flow(
    edges: List[List[int]], source: int, sink: int
) -> Tuple[List[List[int]], int]:
    """Use Ford-Fulkerson to find max flow from source to sink.
    Return the residual graph and the max flow amount.
    """

    N: int = len(edges)
    total_flow: int = 0

    while path := bfs(edges, source, sink):
        path_flow: int = N**3
        # get min edge across path
        for i in range(len(path) - 1):
            curr_node: int = path[i + 1]
            next_node: int = path[i]
            edge_flow: int = edges[curr_node][next_node]
            path_flow = min(edge_flow, path_flow)

        total_flow += path_flow

        # update graph
        for i in range(len(path) - 1):
            curr_node = path[i + 1]
            next_node = path[i]
            edges[curr_node][next_node] -= path_flow
            edges[next_node][curr_node] += path_flow

    return edges, total_flow


def min_cut_partitions(
    edges: List[List[int]], source: int, sink: int
) -> Tuple[Set[int], Set[int]]:
    N: int = len(edges)

    residual, total_flow = max_flow(edges, source, sink)
    distance: List[int] = bfs(residual, source, sink, ret="dist")

    logger.info(f"{total_flow=}")

    visitable_from_source: Set[int] = set(i for i in range(N) if distance[i] != -1)
    visitable_from_sink: Set[int] = set(i for i in range(N) if distance[i] == -1)

    return visitable_from_source, visitable_from_sink


def build_edges(input_lines: List[str]) -> List[List[int]]:
    initial_dict: Dict[str, List[str]] = {}

    for line in input_lines:
        parts: List[str] = line.split(":")
        start: str = parts[0]
        rhs: List[str] = parts[1].strip().split(" ")

        initial_dict[start] = rhs

    name_to_int: Dict[str, int] = {}

    def add_to_dict(my_dict: Dict[str, int], item: str) -> None:
        if item not in my_dict:
            my_dict[item] = len(my_dict)

    for k, rhs in initial_dict.items():
        add_to_dict(name_to_int, k)
        for neighbor in rhs:
            add_to_dict(name_to_int, neighbor)

    names: List[Tuple[str, int]] = [(k, v) for k, v in name_to_int.items()]
    pprint(sorted(names, key=lambda x: x[1]))

    N: int = len(name_to_int)

    edges: List[List[int]] = [[0] * N for i in range(N)]

    for k, rhs in initial_dict.items():
        for neighbor in rhs:
            edges[name_to_int[k]][name_to_int[neighbor]] = 1
            edges[name_to_int[neighbor]][name_to_int[k]] = 1

    return edges


def find_farthest_parts_of_graph(edges: List[List[int]]) -> Tuple[int, int]:
    N: int = len(edges)

    distance_1: List[int] = bfs(edges, 0, -1, ret="dist")
    node_1: int = -1
    highest_dist: int = -1
    for i in range(N):
        if distance_1[i] > highest_dist:
            highest_dist = distance_1[i]
            node_1 = i

    distance_2: List[int] = bfs(edges, node_1, -1, ret="dist")
    node_2: int = -1
    highest_dist = -1
    for i in range(N):
        if distance_2[i] > highest_dist:
            highest_dist = distance_2[i]
            node_2 = i

    return node_1, node_2


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day25.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    edges: List[List[int]] = build_edges(input_lines)
    source, sink = find_farthest_parts_of_graph(edges)
    logger.debug(f"{source=} and {sink=}")

    visitable_from_source, visitable_from_sink = min_cut_partitions(edges, source, sink)

    answer: int = len(visitable_from_source) * len(visitable_from_sink)
    logger.info(f"{answer=}")  # 507626


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
