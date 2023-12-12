ENGLISH_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def process_line(line: str) -> int:
    found_first_digit = False
    first_digit = 0
    last_digit = 0

    for i in range(len(line)):
        current_digit = None
        if "0" <= line[i] <= "9":
            current_digit = ord(line[i]) - ord("0")
        else:
            for word in ENGLISH_DIGITS:
                if i + len(word) <= len(line) and line[i : i + len(word)] == word:
                    current_digit = ENGLISH_DIGITS[word]

        if current_digit is not None:
            if found_first_digit:
                last_digit = current_digit
            else:
                first_digit = last_digit = current_digit
                found_first_digit = True

    return 10 * first_digit + last_digit


def main():
    input_file = "inputs/day01.txt"

    input_lines = []
    with open(input_file, "r") as fd:
        input_lines = fd.readlines()

    answer = 0
    for line in input_lines:
        answer += process_line(line)

    print(f"{answer=}")  # 53268


if __name__ == "__main__":
    main()
