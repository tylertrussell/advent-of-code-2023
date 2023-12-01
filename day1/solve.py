import argparse
import pytest
from typing import Union


def get_digits_from_string(the_string) -> int:
    """Get the first and last digit from a string, combine them to form an int.
    """
    digits = [char for char in the_string if char.isdigit()]
    # these should still be strings; concatenating, not adding
    return int(digits[0] + digits[-1])


DIGITS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def string_matches_digit(the_string, position) -> Union[int, None]:
    for digit_str in DIGITS:
        if the_string[position:position+len(digit_str)] == digit_str:
            return str(DIGITS.index(digit_str) + 1)


def get_digits_from_string_pt_2(the_string) -> int:
    first, last = (None, None)
    for i in range(len(the_string)):
        value = None
        if the_string[i].isdigit():
            value = the_string[i]
        else:
            str_digit_match = string_matches_digit(the_string, i)
            if str_digit_match is not None:
                value = str_digit_match
        if value is not None:
            if first is None:
                first = value
            else:
                last = value
    if last is None:
        last = first
    # these should still be strings; concatenating, not adding
    return int(first + last)


@pytest.mark.parametrize(
    "the_string, expected", [
        ('1abc2', 12),
        ('pqr3stu8vwx', 38),
        ('a1b2c3d4e5f', 15),
        ('treb7uchet', 77)
    ]
)
def test_get_digits_from_string(the_string, expected):
    assert get_digits_from_string(the_string) == expected


@pytest.mark.parametrize(
    "the_string, expected", [
        ('two1nine', 29),
        ('eightwothree', 83),
        ('abcone2threexyz', 13),
        ('xtwone3four', 24),
        ('4nineeightseven2', 42),
        ('zoneight234', 14),
        ('7pqrstsixteen', 76),
    ]
)
def test_get_digits_from_string(the_string, expected):
    assert get_digits_from_string_pt_2(the_string) == expected


def get_lines_from_file(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    return data


def main(args):
    part = args.part
    filename = 'input.txt'
    data = get_lines_from_file(filename)
    total = 0
    for line in data:
        if part == 1:
            total += get_digits_from_string(line)
        if part == 2:
            total += get_digits_from_string_pt_2(line)
    print(total)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('part', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
