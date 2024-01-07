import time
from typing import Dict, Generator, List, Set, Tuple

from loguru import logger

DEBUG: bool = False


class Brick:
    def __init__(
        self, start_brick: Tuple[int, int, int], end_brick: Tuple[int, int, int]
    ) -> None:
        self.start_brick: Tuple[int, int, int] = start_brick
        self.end_brick: Tuple[int, int, int] = end_brick

    def iterate_brick_voxels(self) -> Generator[Tuple[int, int, int], None, None]:
        for x in range(
            min(self.start_brick[0], self.end_brick[0]),
            1 + max(self.start_brick[0], self.end_brick[0]),
        ):
            for y in range(
                min(self.start_brick[1], self.end_brick[1]),
                1 + max(self.start_brick[1], self.end_brick[1]),
            ):
                for z in range(
                    min(self.start_brick[2], self.end_brick[2]),
                    1 + max(self.start_brick[2], self.end_brick[2]),
                ):
                    yield (x, y, z)

    def move_down(self, amount: int = 1) -> None:
        self.start_brick = (
            self.start_brick[0],
            self.start_brick[1],
            self.start_brick[2] - amount,
        )
        self.end_brick = (
            self.end_brick[0],
            self.end_brick[1],
            self.end_brick[2] - amount,
        )

    def lowest_z_layer(self) -> int:
        return min(self.start_brick[2], self.end_brick[2])

    def xy_coords(self) -> Set[Tuple[int, int]]:
        return {(voxel[0], voxel[1]) for voxel in self.iterate_brick_voxels()}

    def __str__(self) -> str:
        return f"Brick({self.start_brick}, {self.end_brick})"


class Node:
    def __init__(self, index: int) -> None:
        self.index = index
        self.inputs: Set[int] = set()
        self.outputs: Set[int] = set()


def bricks_fall_down(bricks: List[Brick]) -> Dict[Tuple[int, int, int], int]:
    space_occupied: Dict[Tuple[int, int, int], int] = {}

    for brick_index, brick in enumerate(bricks):
        for voxel in brick.iterate_brick_voxels():
            space_occupied[voxel] = brick_index

    something_moved: bool = True
    while something_moved:
        something_moved = False

        for brick_index, brick in enumerate(bricks):
            current_brick_moved: bool = True

            while current_brick_moved:
                current_brick_moved = False

                # check if space underneath is occupied
                layer_to_check: int = brick.lowest_z_layer() - 1
                if layer_to_check == 0:
                    break

                lower_layer_empty: bool = all(
                    (xy[0], xy[1], layer_to_check) not in space_occupied
                    for xy in brick.xy_coords()
                )
                if lower_layer_empty:
                    for voxel in brick.iterate_brick_voxels():
                        del space_occupied[voxel]
                    brick.move_down()
                    current_brick_moved = True
                    something_moved = True
                    for voxel in brick.iterate_brick_voxels():
                        space_occupied[voxel] = brick_index

    return space_occupied


def generate_graph(
    bricks: List[Brick], space_occupied: Dict[Tuple[int, int, int], int]
) -> List[Node]:
    N: int = len(bricks)

    nodes: List[Node] = [Node(i) for i in range(N)]

    for voxel, brick_index in space_occupied.items():
        # check beneath: if there is something B that is not itself, B supports this current voxel
        lower_voxel: Tuple[int, int, int] = (voxel[0], voxel[1], voxel[2] - 1)
        if lower_voxel in space_occupied:
            lower_brick_index: int = space_occupied[lower_voxel]
            if lower_brick_index != brick_index:
                # lower supports upper
                nodes[lower_brick_index].outputs.add(brick_index)
                nodes[brick_index].inputs.add(lower_brick_index)

    return nodes


def check_safe_to_disintegrate(nodes: List[Node], brick_index: int) -> bool:
    """Either current brick does not support any, or it does, and all of its supported
    can be supported by another brick.
    """
    if len(nodes[brick_index].outputs) == 0:
        return True

    return all(
        len(nodes[higher_brick_index].inputs) > 1
        for higher_brick_index in nodes[brick_index].outputs
    )


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day22.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    bricks: List[Brick] = []
    for line in input_lines:
        coord1_repr, coord2_repr = line.split("~", 1)

        coord1_split: List[str] = coord1_repr.split(",")
        coord2_split: List[str] = coord2_repr.split(",")

        coord1: Tuple[int, int, int] = (
            int(coord1_split[0]),
            int(coord1_split[1]),
            int(coord1_split[2]),
        )
        coord2: Tuple[int, int, int] = (
            int(coord2_split[0]),
            int(coord2_split[1]),
            int(coord2_split[2]),
        )

        bricks.append(Brick(coord1, coord2))

    #  logger.info(f"Before falling, have coords {[str(brick) for brick in bricks]}")

    space_occupied: Dict[Tuple[int, int, int], int] = bricks_fall_down(bricks)

    #  logger.info(f"After falling, have coords {[str(brick) for brick in bricks]}")

    nodes: List[Node] = generate_graph(bricks, space_occupied)

    num_nodes_can_be_safely_disintegrated: int = 0
    for brick_index in range(len(nodes)):
        if check_safe_to_disintegrate(nodes, brick_index):
            num_nodes_can_be_safely_disintegrated += 1

    answer: int = num_nodes_can_be_safely_disintegrated
    logger.info(f"{answer=}")  # 448


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
