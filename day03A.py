from typing import List

DEBUG = False

def valid(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def print_board(board):
    for row in board:
        for c in row:
            if c:
                print('1', end='')
            else:
                print('0', end='')
        print()


def process_board(board: List[str]) -> int:
    R = len(board)
    C = len(board[0])

    good_digits = [[False for c in range(C)] for r in range(R)]

    for row in range(R):
        for col in range(C):
            c = board[row][col]

            if c != '.' and not ('0' <= c <= '9'):
                # is symbol

                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if valid(row + dr, col + dc, R, C) and '0' <= board[row + dr][col + dc] <= '9':
                            good_digits[row + dr][col + dc] = True

    print_board(good_digits)

    for row in range(R):
        for c in range(1, C):
            if '0' <= board[row][c] <= '9' and good_digits[row][c - 1]:
                good_digits[row][c] = True

        for c in range(C - 2, -1, -1):
            if '0' <= board[row][c] <= '9' and good_digits[row][c + 1]:
                good_digits[row][c] = True

    print("now")
    print_board(good_digits)

    answer = 0

    for row in range(R):
        my_num = 0
        for c in range(C):
            if good_digits[row][c]:
                digit = ord(board[row][c]) - ord('0')
                my_num = 10 * my_num + digit
            else:
                answer += my_num
                my_num = 0

        answer += my_num
        my_num = 0

    return answer


def main():
    input_file = 'inputs/day03.txt'

    if DEBUG:
        input_file = 'inputs/dummy.txt'

    input_lines = []
    with open(input_file, 'r') as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    answer = process_board(input_lines)

    print(f'{answer=}')  # 538046


if __name__ == '__main__':
    main()
