import argparse


# (horizontal, vertical)
VALID_DELTAS = [
    (1, -1),
    (1, 0),
    (1, 1),
    (0, -1),
    (0, 1),
    (-1, -1),
    (-1, 0),
    (-1, 1)
]


def is_symbol(char):
    return char != '.' and not char.isnumeric() and not char.isalpha()


def read_input(input_file):
    with open(input_file, 'r') as f:
        return f.readlines()


def parse_args():
    parser = argparse.ArgumentParser(description='Solve the problem')
    parser.add_argument('input_file', type=str, help='input file')
    args = parser.parse_args()
    return args


def is_part_number(row: int, col: int, length: int, data: list) -> bool:
    """Given a number's position, determine if it's a part number.

    Args:
        row: row index for part number
        col: col index for part number (start)
        length: length of part number
        data: full data set

    Returns: bool
    """
    for col in range(col, col + length):
        for row_d, col_d in VALID_DELTAS:
            target_ridx = row + row_d
            target_cidx = col + col_d
            if target_ridx < 0 or target_ridx >= len(data) or target_cidx < 0 or target_cidx >= len(data[target_ridx]):
                continue
            char = data[target_ridx][target_cidx]
            if is_symbol(char):
                print(f"symbol {char} at delta {row_d},{col_d}")
                return True
    return False


def test_is_part_number():
    data = read_input("test_input.txt")
    assert is_part_number(0, 0, 3, data) is True  # 467 in row 1
    assert is_part_number(0, 5, 3, data) is False  # 114 in row 1


def get_next_number(input_line: str, start_search_at: int) -> (str, int, int):
    """
    Scan an input line for a number, starting at the given index.

    n.b. does not check to see if the number is a part number.

    Args:
        input_line:  str full input line
        start_search_at:  int index to start searching at; not necessarily a number
    Returns:
        tuple of:
            number string (no guarantee it's a part number!)
            start column
            index to start next search
    """
    # record boundaries of the next part number we find
    start_col = None
    end_col = None

    for cidx in range(start_search_at, len(input_line)):
        char = input_line[cidx]
        if char.isnumeric():
            # record the start position index
            if start_col is None:
                start_col = cidx
                continue

            # edge case: number is at the end of the line, so set end pos
            if cidx == len(input_line) - 1:
                print("last thing edge case")
                # note we add 1 here because this is the end of the line only
                end_col = cidx + 1
                break
        else:
            # record end position index
            if start_col is not None:
                end_col = cidx
                break

    # only return part number and column if we actually found something
    if start_col is not None:
        # edge case: number is at the end of the line, so set end pos
        if end_col is None:
          end_col = start_col + 1
        number = input_line[start_col:end_col]
        return number, start_col, end_col

    return None, None, None


def test_get_next_number():
    input_str = "467..114.."
    part_number, start_col, end_col = get_next_number(input_str, 0)
    assert part_number == "467"
    assert start_col == 0
    assert end_col == 3
    part_number, start_col, end_col = get_next_number(input_str, end_col)
    assert part_number == "114"
    assert start_col == 5
    assert end_col == 8
    part_number, start_col, end_col = get_next_number(input_str, end_col)
    assert part_number is None
    assert start_col is None
    assert end_col is None
    long_input_str = '.....510'
    part_number, start_col, end_col = get_next_number(long_input_str, 0)
    assert part_number == "510"
    assert start_col == 5
    assert end_col == 8
    single_end_input_str = '.1.1'
    part_number, start_col, end_col = get_next_number(single_end_input_str, 0)
    assert part_number == "1"
    assert start_col == 1
    assert end_col == 2
    part_number, start_col, end_col = get_next_number(single_end_input_str, end_col)
    assert part_number == "1"
    assert start_col == 3
    assert end_col == 4


def part_one_solution(data):
    # track all the part numbers we find along the way
    part_numbers = list()

    for ridx in range(0, len(data)):
        line = data[ridx]
        print(line)

        # find each number in the row and check if its a part number
        search_col = 0
        while search_col is not None:
            number_str, start_col, end_col = get_next_number(line, search_col)
            if number_str is not None and is_part_number(ridx, start_col, len(number_str), data):
                part_numbers.append(int(number_str))
                print(f"part number {number_str} at pos {start_col}")
            else:
                print(f"not a part number: {number_str}")
            search_col = end_col

    return sum(part_numbers)


def test_part_one_solution():
    data = read_input("test_input.txt")
    assert part_one_solution(data) == 4361 + 912  # I added 912 as an edge case
    # reddit data
    data = read_input("test_input2.txt") == 413 + 1  # I added 1 as an edge case


def main():
    args = parse_args()
    print(part_one_solution(read_input(args.input_file)))


if __name__ == "__main__":
    main()
