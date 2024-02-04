"""
Pxr = initial x position of rock
Vyhi = y component of velocity of hailstone i

Both hailstone i and rock collide at time Ti
VxhiTi + Pxhi = VxrTi + Pxr
Isolate Ti:
Ti = (Pxr - Pxhi) / (Vxhi - Vxr)
and same for components y and z
Since same, multiply denominators:

1) PxrVyhi - PxhiVyhi - PxrVyr + PxhiVyr = PyrVxhi - PyhiVxhi - PyrVxr＋PyhiVxr
2) PxrVzhi - PxhiVzhi - PxrVzr + PxhiVzr = PzrVxhi - PzhiVxhi - PzrVxr + PzhiVxr
3) PxrVyhj - PxhjVyhj - PxrVyr + PxhjVyr = PyrVxhj - PyhjVxhj - PyrVxr＋PyhjVxr
4) PxrVzhj - PxhjVzhj - PxrVzr + PxhjVzr = PzrVxhj - PzhjVxhj - PzrVxr + PzhjVxr

1) - 3):
Pxr(Vyhi - Vyhj) - PxhiVyhi + PxhjVyhj + Vyr(Pxhi - Pxhj) = Pyr(Vxhi - Vxhj) - PyhiVxhi + PyhjVxhj + Vxr(Pyhi - Pyhj)
or
Pxr(Vyhi - Vyhj) - Pyr(Vxhi - Vxhj) - Vxr(Pyhi - Pyhj) + Vyr(Pxhi - Pxhj) = PxhiVyhi - PxhjVyhj - PyhiVxhi + PyhjVxhj
2) - 4)
Pxr(Vzhi - Vzhj) - PxhiVzhi + PxhjVzhj + Vzr(Pxhi - Pxhj) = Pzr(Vxhi - Vxhj) - PzhiVxhi + PzhjVxhj + Vxr(Pzhi - Pzhj)
or
Pxr(Vzhi - Vzhj) - Pzr(Vxhi - Vxhj) - Vxr(Pzhi - Pzhj) + Vzr(Pxhi - Pxhj) = PxhiVzhi - PxhjVzhj - PzhiVxhi + PzhjVxhj

Get 6 equations with 4 hailstones: hail 0 with hail 1 generates 2. Then hail 0 with hail 2, and hail 0 with hail 3.
Then, treat as linear system of equations with 6 unknowns:
Pxr, Pyr, Pzr, Vxr, Vyr, Vzr.
"""

import time
from pprint import pprint
from typing import List, Tuple

from loguru import logger

DEBUG: bool = False


def get_two_equations(
    hailstone_i: Tuple[Tuple[int, int, int], Tuple[int, int, int]],
    hailstone_j: Tuple[Tuple[int, int, int], Tuple[int, int, int]],
) -> Tuple[List[int], int, List[int], int]:
    Pxhi: int = hailstone_i[0][0]
    Pyhi: int = hailstone_i[0][1]
    Pzhi: int = hailstone_i[0][2]
    Vxhi: int = hailstone_i[1][0]
    Vyhi: int = hailstone_i[1][1]
    Vzhi: int = hailstone_i[1][2]

    Pxhj: int = hailstone_j[0][0]
    Pyhj: int = hailstone_j[0][1]
    Pzhj: int = hailstone_j[0][2]
    Vxhj: int = hailstone_j[1][0]
    Vyhj: int = hailstone_j[1][1]
    Vzhj: int = hailstone_j[1][2]

    equation_1: List[int] = [Vyhi - Vyhj, -Vxhi + Vxhj, 0, -Pyhi + Pyhj, Pxhi - Pxhj, 0]
    b_1: int = Pxhi * Vyhi - Pxhj * Vyhj - Pyhi * Vxhi + Pyhj * Vxhj
    equation_2: List[int] = [Vzhi - Vzhj, 0, -Vxhi + Vxhj, -Pzhi + Pzhj, 0, Pxhi - Pxhj]
    b_2: int = Pxhi * Vzhi - Pxhj * Vzhj - Pzhi * Vxhi + Pzhj * Vxhj

    return (equation_1, b_1, equation_2, b_2)


def get_coefficient_matrix_and_b(
    hailstones: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]
) -> Tuple[List[List[int]], List[int]]:
    coefficient_matrix: List[List[int]] = []
    b_vector: List[int] = []

    for i in (1, 2, 3):
        hailstone_i = hailstones[0]
        hailstone_j = hailstones[i]
        two_equations: Tuple[List[int], int, List[int], int] = get_two_equations(
            hailstone_i, hailstone_j
        )
        coefficient_matrix.append(two_equations[0])
        coefficient_matrix.append(two_equations[2])
        b_vector.append(two_equations[1])
        b_vector.append(two_equations[3])

    return (coefficient_matrix, b_vector)


def gaussian_elimination(
    coefficient_matrix_int: List[List[int]], b_vector_int: List[int]
) -> List[float]:
    pprint(coefficient_matrix_int)
    pprint(b_vector_int)

    coefficient_matrix: List[List[float]] = [
        [float(x) for x in row] for row in coefficient_matrix_int
    ]
    b_vector: List[float] = [float(x) for x in b_vector_int]
    N: int = len(coefficient_matrix)

    for i in range(N):
        # first ensure coefficient_matrix[i][i] is non-zero. If not, swap with a lower row
        for j in range(i, N):
            if coefficient_matrix[j][i] != 0:
                temp_row: List[float] = coefficient_matrix[i]
                coefficient_matrix[i] = coefficient_matrix[j]
                coefficient_matrix[j] = temp_row

                temp_b: float = b_vector[i]
                b_vector[i] = b_vector[j]
                b_vector[j] = temp_b

        # normalize row i by setting row_i[i] to be 1
        divisor: float = coefficient_matrix[i][i]
        for j in range(N):
            coefficient_matrix[i][j] /= divisor
        b_vector[i] /= divisor

        # now ensure for all other rows j, that row_j[i] is 0
        for row_index in range(N):
            if row_index == i:
                continue
            other_row: List[float] = coefficient_matrix[row_index]

            multiplier: float = other_row[i]
            for col_index in range(N):
                other_row[col_index] -= multiplier * coefficient_matrix[i][col_index]
            b_vector[row_index] -= multiplier * b_vector[i]

    return b_vector


def calc_rock_position_and_velocity(
    hailstones: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    coefficient_matrix, b_vector = get_coefficient_matrix_and_b(hailstones)
    x_vector = gaussian_elimination(coefficient_matrix, b_vector)

    rock_position: Tuple[float, float, float] = (x_vector[0], x_vector[1], x_vector[2])
    rock_velocity: Tuple[float, float, float] = (x_vector[3], x_vector[4], x_vector[5])

    return (rock_position, rock_velocity)


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day24.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    hail: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = []
    for line in input_lines:
        pos, vel = line.split("@", 1)

        position_str: List[str] = pos.split(", ", 2)
        velocity_str: List[str] = vel.split(", ", 2)

        position: Tuple[int, int, int] = (
            int(position_str[0]),
            int(position_str[1]),
            int(position_str[2]),
        )
        velocity: Tuple[int, int, int] = (
            int(velocity_str[0]),
            int(velocity_str[1]),
            int(velocity_str[2]),
        )
        hail.append((position, velocity))

    rock_initial_position, rock_velocity = calc_rock_position_and_velocity(hail)

    logger.info(
        f"rock position = {rock_initial_position} and velocity = {rock_velocity}"
    )

    answer: int = round(
        rock_initial_position[0] + rock_initial_position[1] + rock_initial_position[2]
    )
    logger.info(f"{answer=}")  # 856642398547748

    # rock position = (422644646660238.0, 244357651988392.0, 189640099899118.12)
    # and velocity = (-260.0000000000001, 34.00000000000006, 181.00000000000006)


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
