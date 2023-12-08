from typing import List, Tuple

DEBUG = False

def game_power(subsets: List[Tuple[int, int, int]]) -> int:
    best = [0, 0, 0]

    for subset in subsets:
        for i in range(3):
            best[i] = max(best[i], subset[i])

    return best[0] * best[1] * best[2]


def main():
    input_file = 'inputs/day02.txt'

    if DEBUG:
        input_file = 'inputs/dummy.txt'

    input_lines = []
    with open(input_file, 'r') as fd:
        input_lines = fd.readlines()

    answer = 0
    for line in input_lines:
        id_start_index = len('Game ')
        id_end_index = line.find(':')

        game_subsets = []

        game_id: int = int(line[id_start_index:id_end_index])

        game_line = line[id_end_index + len(': '):]
        game_subset_lines: List[str] = game_line.split('; ')

        for game_subset_line in game_subset_lines:
            # "1 blue, 2 green"
            split_colors = game_subset_line.split(', ')
            # ['1 blue', '2 green']

            num_red = 0
            num_green = 0
            num_blue = 0

            for num_and_color in split_colors:
                # '1 blue'
                num_and_color_split = num_and_color.strip().split(' ')
                num_color = int(num_and_color_split[0])
                color_name = num_and_color_split[1]

                if color_name == 'red':
                    num_red += num_color
                elif color_name == 'green':
                    num_green += num_color
                elif color_name == 'blue':
                    num_blue += num_color

            game_subsets.append((num_red, num_green, num_blue))

        print(f'{game_subsets=}')
        answer += game_power(game_subsets)

    print(f'{answer=}')  # 62241


if __name__ == '__main__':
    main()
