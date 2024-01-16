import time
from fractions import Fraction
from typing import List, Optional, Tuple

from loguru import logger

DEBUG: bool = False

LOWER_BOUND: int = 200000000000000
UPPER_BOUND: int = 400000000000000

if DEBUG:
    LOWER_BOUND = 7
    UPPER_BOUND = 27


def generate_intersection(
    pos_a: Tuple[int, int, int],
    vel_a: Tuple[int, int, int],
    pos_b: Tuple[int, int, int],
    vel_b: Tuple[int, int, int],
) -> Optional[Tuple[Fraction, Fraction, Fraction]]:
    #  logger.info(f'Find intersection of {pos_a=} {vel_a=} with {pos_b=} {vel_b=}')

    a: int = -vel_a[0]
    b: int = vel_b[0]
    c: int = -vel_a[1]
    d: int = vel_b[1]

    rhs: Tuple[int, int] = (pos_a[0] - pos_b[0], pos_a[1] - pos_b[1])

    determinant: int = a * d - b * c

    a_prime: int = d
    d_prime: int = a
    b_prime: int = -b
    c_prime: int = -c

    #  logger.debug(f'{a=} {b=} {c=} {d=}')
    #  logger.debug(f'{determinant=}')

    if determinant == 0:
        return None

    t_a: Fraction = Fraction(1, determinant) * (a_prime * rhs[0] + b_prime * rhs[1])
    t_b: Fraction = Fraction(1, determinant) * (c_prime * rhs[0] + d_prime * rhs[1])

    #  logger.debug(f'{t_a=} {t_b=}')

    if t_a >= 0 and t_b >= 0:
        projected_position_a: Tuple[Fraction, Fraction, Fraction] = (
            vel_a[0] * t_a + pos_a[0],
            vel_a[1] * t_a + pos_a[1],
            vel_a[2] * t_a + pos_a[2],
        )
        projected_position_b: Tuple[Fraction, Fraction, Fraction] = (
            vel_b[0] * t_b + pos_b[0],
            vel_b[1] * t_b + pos_b[1],
            vel_b[2] * t_b + pos_b[2],
        )

        diff: Fraction = abs(projected_position_b[0] - projected_position_a[0]) + abs(
            projected_position_b[1] - projected_position_a[1]
        )

        if diff == 0:
            return projected_position_a

    return None


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

    answer: int = 0

    for i in range(len(hail)):
        for j in range(i + 1, len(hail)):
            intersection: Optional[
                Tuple[Fraction, Fraction, Fraction]
            ] = generate_intersection(hail[i][0], hail[i][1], hail[j][0], hail[j][1])

            if intersection is not None:
                logger.debug(f"Hail {i} and {j} intersect at {intersection}")

                if all(LOWER_BOUND <= intersection[i] <= UPPER_BOUND for i in range(2)):
                    answer += 1

    logger.info(f"{answer=}")  # 15107


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
