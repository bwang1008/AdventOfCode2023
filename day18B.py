import time
from typing import List, Tuple

from loguru import logger

DEBUG: bool = False

RIGHT: int = 0
DOWN: int = 1
LEFT: int = 2
UP: int = 3


def hex_to_decimal(hex_code: str) -> int:
    answer: int = 0
    for char in hex_code:
        digit: int = 0
        if "a" <= char <= "f":
            digit = 10 + ord(char) - ord("a")
        else:
            digit = int(char)

        answer = 16 * answer + digit

    return answer


def move_position(
    position: Tuple[int, int], direction: int, amount: int
) -> Tuple[int, int]:
    if direction == RIGHT:
        return (position[0], position[1] + amount)
    if direction == UP:
        return (position[0] - amount, position[1])
    if direction == LEFT:
        return (position[0], position[1] - amount)

    # DOWN
    return (position[0] + amount, position[1])


def area_and_perimeter(coordinates: List[Tuple[int, int]]) -> Tuple[int, int]:
    area: int = 0
    exterior_length: int = 0

    for i in range(len(coordinates)):
        curr_coord: Tuple[int, int] = coordinates[i]
        next_coord: Tuple[int, int] = coordinates[(i + 1) % len(coordinates)]

        area += curr_coord[0] * next_coord[1] - curr_coord[1] * next_coord[0]
        exterior_length += abs(next_coord[0] - curr_coord[0]) + abs(
            next_coord[1] - curr_coord[1]
        )

    return (abs(area // 2), exterior_length)


def calc_area(instructions: List[Tuple[int, int]]) -> int:
    coordinates: List[Tuple[int, int]] = [(0, 0)]
    for index, instruction in enumerate(instructions):
        # a loop, so last coordinate is also the origin
        if index != len(instructions) - 1:
            coordinates.append(
                move_position(coordinates[-1], instruction[0], instruction[1])
            )

    logger.debug(f"Coordinates = {coordinates}")

    area, exterior_length = area_and_perimeter(coordinates)

    # Pick's theorem
    num_interior_points: int = area + 1 - exterior_length // 2

    logger.debug(f"Have {area=} and {exterior_length=} and {num_interior_points=}")

    return exterior_length + num_interior_points


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day18.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    instructions: List[Tuple[int, int]] = []
    for line in input_lines:
        hash_index: int = line.find("#")
        hex_code: str = line[hash_index + 1 : hash_index + 7]
        instructions.append(
            (
                int(hex_code[-1]),
                hex_to_decimal(hex_code[:5]),
            )
        )

    answer: int = calc_area(instructions)
    logger.info(f"{answer=}")  # 82712746433310


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
