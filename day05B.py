import time
from pprint import pprint
from typing import List, Tuple

from loguru import logger

DEBUG = False

def get_range_diff(input_range: Tuple[int, int], subsets: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Ex: given input_range = (5, 7)  (meaning numbers 5,6,7,8,9,10,11), and subsets
    [(5, 3), (10, 1))] (meaning numbers 5,6,7,10), return
    [(8, 2), (11, 1)] (meaning numbers 8,9,11).

    Assume subsets is sorted.
    """

    missing_ranges: List[Tuple[int, int]] = []

    input_range_index = input_range[0]
    subset_index = 0

    while input_range_index < input_range[0] + input_range[1]:
        if subset_index == len(subsets):
            missing_ranges.append((input_range_index, input_range[0] + input_range[1] - input_range_index))
            break
        # ex: if 5 from (5, 7) is less than the 5 from (5, 3)
        if input_range_index < subsets[subset_index][0]:
            missing_ranges.append((input_range_index, subsets[subset_index][0] - input_range_index))
            input_range_index = subsets[subset_index][0]
        else:
            # pre-condition that input_range_index <= current subset start range
            # so currently, they are equal; skip this subset
            input_range_index = subsets[subset_index][0] + subsets[subset_index][1]
            subset_index += 1

    return missing_ranges

def get_single_mapped_value(input_key: int, mapping: Tuple[int, int, int]) -> int:
    dest, source, length = mapping

    if input_key in range(source, source + length):
        return dest +  (input_key - source)

    return input_key


def get_mapped_value(input_range: Tuple[int, int], mapping: List[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
    """Given an input range of seed values (like for seeds [5, 12] would have input_range = (5, 7)),
    use the mapping provided to get, for instance, the soil-type ranges.
    """

    logger.debug(f'get_mapped_value({input_range=})')

    intersection_ranges: List[Tuple[int, int]] = []

    # to be returned
    resulting_output_ranges: List[Tuple[int, int]] = []

    # use each mapping to break up each input_range
    for tups in mapping:
        dest, source, length = tups

        # break up input_range across mapping's source range
        # this is mathematical range, not (start, length)
        source_range_intersection: Tuple[int, int] = max(source, input_range[0]), min(source + length, input_range[0] + input_range[1])

        # has to be a valid intersection range
        if source_range_intersection[0] >= source_range_intersection[1]:
            continue

        logger.debug(f'mapping={tups} resulted in {source_range_intersection}')

        intersection_ranges.append((source_range_intersection[0], source_range_intersection[1] - source_range_intersection[0]))
        resulting_output_ranges.append(
                (get_single_mapped_value(source_range_intersection[0], tups),
                    source_range_intersection[1] - source_range_intersection[0]
                )
        )

    intersection_ranges.sort()

    not_intersected: List[Tuple[int, int]] = get_range_diff(input_range, intersection_ranges)

    logger.debug(f'{resulting_output_ranges=}')

    # those not intersected, get mapped to output via identity

    return resulting_output_ranges + not_intersected


def get_all_attributes(seed_ranges: List[Tuple[int, int]], mappings: List[List[Tuple[int, int, int]]]) -> List[List[List[Tuple[int, int]]]]:
    all_seed_attributes: List[List[List[Tuple[int, int]]]] = [[[seed_range]] for seed_range in seed_ranges]
    # for example, all_seed_attributes[0] would be all attribute ranges of seed_range 0.
    # each attribute of seed_range 0 is a list of ranges

    for mapping in mappings:
        for seed_index in range(len(seed_ranges)):
            all_output_attributes = []
            # iterate across all of the ranges in the latest attribute
            for input_range in all_seed_attributes[seed_index][-1]:
                output_attributes: List[Tuple[int, int]] = get_mapped_value(input_range, mapping)
                all_output_attributes.extend(output_attributes)

            all_seed_attributes[seed_index].append(all_output_attributes)

    return all_seed_attributes


def get_min_location(seed_ranges: List[Tuple[int, int]], mappings: List[List[Tuple[int, int, int]]]) -> int:
    all_seed_attributes: List[List[List[Tuple[int, int]]]] = get_all_attributes(seed_ranges, mappings)

    logger.debug(f'{all_seed_attributes=}')

    return min(output_ranges[0] for seed_all_attributes_ranges in all_seed_attributes for output_ranges in seed_all_attributes_ranges[-1])


def main() -> None:
    input_file = 'inputs/day05.txt'

    if DEBUG:
        input_file = 'inputs/dummy.txt'

    input_lines = []
    with open(input_file, 'r') as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    seeds = [int(s) for s in input_lines[0][len('seeds: '):].split(' ')]
    seed_ranges: List[Tuple[int, int]] = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]

    attribute_maps: List[List[Tuple[int, int, int]]] = []

    line_index = 1
    for line_index, line in enumerate(input_lines):
        if line_index == 0:
            continue

        line = input_lines[line_index]

        if line == '':
            line_index += 1
        elif line.endswith(':'):
            attribute_maps.append([])
        else:
            nums = [int(s) for s in line.split(' ')]
            attribute_maps[-1].append((nums[0], nums[1], nums[2]))

    logger.debug(f'{seeds=}')
    logger.debug(f'{attribute_maps}')

    answer = get_min_location(seed_ranges, attribute_maps)
    logger.info(f'{answer=}')  # 77435348


if __name__ == '__main__':
    start_time = time.time()
    main()

    logger.info(f'Took {time.time() - start_time}')
