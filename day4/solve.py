import argparse
import pytest

from collections import defaultdict


def parse_line(line) -> (set[int], set[int]):
    card, remainder = line.split(': ')
    raw_winning_nos, raw_my_nos = remainder.split(' | ')
    winning_nos = {int(x.strip()) for x in raw_winning_nos.split(' ') if x != ''}
    my_nos = {int(x.strip()) for x in raw_my_nos.split(' ') if x != ''}
    return winning_nos, my_nos


@pytest.mark.parametrize(
    "line, expected",
    [
        ("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53", ({41, 48, 83, 86, 17}, {83, 86, 6, 31, 17, 9, 48, 53})),
        ("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", ({13, 32, 20, 16, 61}, {61, 30, 68, 82, 17, 32, 24, 19})),
        # ("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        # ("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        # ("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        # ("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]
)
def test_parse_line(line, expected):
    assert parse_line(line) == expected


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='input file')
    parser.add_argument('mode', type=int, help='output file')
    return parser.parse_args()


def number_of_winners(winning_nos, my_nos):
    return len(my_nos.intersection(winning_nos))


def solution_one(data):
    ttl_value = 0
    for line in data:
        winning_nos, my_nos = parse_line(line)
        winners = number_of_winners(winning_nos, my_nos)
        if winners == 0:
            continue
        # doubling every time is the same as 2 ^ n - 1 (except 0)
        value = 2 ** (winners - 1)
        ttl_value += value
    return ttl_value


def solution_two(data):
    copy_counter = defaultdict(int)
    for idx in range(0, len(data)):
        line = data[idx]
        winning_nos, my_nos = parse_line(line)
        winners = number_of_winners(winning_nos, my_nos)
        if winners == 0:
            continue
        # add copies of subsequent cards for each winner
        for i in range(idx + 1, idx + 1 + winners):
            # add one + the number of copies we've got of this card
            num_copies = 1 + copy_counter[idx]
            copy_counter[i] += num_copies
    return sum(copy_counter.values()) + len(data)  # add the number of non-copies


def test_solution_two():
    data = read_input('test_input.txt')
    assert solution_two(data) == 30


def test_solution_one():
    data = read_input("test_input.txt")
    assert solution_one(data) == 13


def read_input(input_file):
    with open(input_file, 'r') as f:
        return [line.strip() for line in f.readlines()]


MODE_MAP = {
    1: solution_one,
    2: solution_two,
}

def main():
    args = parse_args()
    func = MODE_MAP[args.mode]
    data = read_input(args.input_file)
    print(func(data))


if __name__ == '__main__':
    main()
