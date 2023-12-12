from typing import List

DEBUG = False


def valid(r, c, R, C):
    return 0 <= r < R and 0 <= c < C


def print_board(board):
    for row in board:
        for c in row:
            if c:
                print("1", end="")
            else:
                print("0", end="")
        print()


def process_board(board: List[str]) -> int:
    R = len(board)
    C = len(board[0])

    used = [[False for c in range(C)] for r in range(R)]

    answer = 0

    for row in range(R):
        for col in range(C):
            c = board[row][col]

            if c != "." and not ("0" <= c <= "9"):
                # is symbol

                parts = []

                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if (
                            valid(row + dr, col + dc, R, C)
                            and "0" <= board[row + dr][col + dc] <= "9"
                            and not used[row + dr][col + dc]
                        ):
                            new_row = row + dr
                            new_col = col + dc

                            # expand it first; set to "used" in used
                            used[new_row][new_col] = True
                            right_col = new_col + 1
                            while (
                                right_col < C
                                and "0" <= board[new_row][right_col] <= "9"
                            ):
                                used[new_row][right_col] = True
                                right_col += 1

                            left_col = new_col - 1
                            while (
                                left_col >= 0 and "0" <= board[new_row][left_col] <= "9"
                            ):
                                used[new_row][left_col] = True
                                left_col -= 1

                            part_value = 0
                            for i in range(left_col + 1, right_col):
                                part_value = (
                                    10 * part_value + ord(board[new_row][i]) - ord("0")
                                )

                            parts.append(part_value)

                print(f"At {row=}, {col=}, we have {parts=}")

                if len(parts) == 2:
                    answer += parts[0] * parts[1]

    return answer


def main():
    input_file = "inputs/day03.txt"

    if DEBUG:
        input_file = "inputs/dummy.txt"

    input_lines = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    answer = process_board(input_lines)

    print(f"{answer=}")  # 81709807


if __name__ == "__main__":
    main()
