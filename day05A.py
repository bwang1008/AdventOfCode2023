from typing import List, Tuple

from loguru import logger

DEBUG = False

def get_mapped_value(input_key: int, mapping: List[Tuple[int, int, int]]) -> int:
    for tups in mapping:
        dest, source, length = tups

        if input_key in range(source, source + length):
            return dest + (input_key - source)

    return input_key

def get_all_attributes(seeds: List[int], mappings: List[List[Tuple[int, int, int]]]):
    all_seed_attributes: List[List[int]] = [[seed] for seed in seeds]

    for mapping in mappings:
        for seed_index in range(len(seeds)):
            input_key: int = all_seed_attributes[seed_index][-1]
            output_value: int = get_mapped_value(input_key, mapping)
            all_seed_attributes[seed_index].append(output_value)

    return all_seed_attributes


def get_min_location(seeds: List[int], mappings: List[List[Tuple[int, int, int]]]):
    all_seed_attributes = get_all_attributes(seeds, mappings)

    logger.debug(f'{all_seed_attributes}')

    return min(seed_attribute[-1] for seed_attribute in all_seed_attributes)


def main():
    input_file = 'inputs/day05.txt'

    if DEBUG:
        input_file = 'inputs/dummy.txt'

    input_lines = []
    with open(input_file, 'r') as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    seeds = [int(s) for s in input_lines[0][len('seeds: '):].split(' ')]

    attribute_maps: List[List[Tuple[int, int, int]]] = [[]]

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

    answer = get_min_location(seeds, attribute_maps)
    logger.info(f'{answer=}')  # 910845529


if __name__ == '__main__':
    main()
