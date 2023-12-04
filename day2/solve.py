import argparse
import pytest
import functools
import operator


PART_ONE_CUBE_LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def _parse_game_id(input_line) -> int:
    GAME = "Game "
    assert input_line.startswith(GAME)
    return int(input_line[len(GAME) :])


@pytest.mark.parametrize(
    "input_line, expected",
    [
        ("Game 1", 1),
        ("Game 2", 2),
        ("Game 3", 3),
    ],
)
def test_parse_game_id(input_line, expected):
    assert _parse_game_id(input_line) == expected


def _parse_reveals(input_line: str) -> list[dict]:
    reveals = []
    str_reveals = input_line.split("; ")
    for str_reveal in str_reveals:
        counts = {}
        for color_reveal in str_reveal.split(", "):
            count, color = color_reveal.split(" ")
            counts[color] = int(count)
        reveals.append(counts)
    return reveals


@pytest.mark.parametrize(
    "input_line, expected",
    [
        (
            "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
            [{"blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, {"green": 2}],
        ),
        (
            "1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
            [
                {"blue": 1, "green": 2},
                {"green": 3, "blue": 4, "red": 1},
                {"green": 1, "blue": 1},
            ],
        ),
        (
            "8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
            [
                {"green": 8, "blue": 6, "red": 20},
                {"blue": 5, "red": 4, "green": 13},
                {"green": 5, "red": 1},
            ],
        ),
        (
            "1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
            [
                {"green": 1, "red": 3, "blue": 6},
                {"green": 3, "red": 6},
                {"green": 3, "blue": 15, "red": 14},
            ],
        ),
        (
            "6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
            [{"red": 6, "blue": 1, "green": 3}, {"blue": 2, "red": 1, "green": 2}],
        ),
    ],
)
def test_parse_reveals(input_line, expected):
    assert _parse_reveals(input_line) == expected


def parse_line(input_line) -> (int, list[dict]):
    game_id_str, reveals_str = input_line.split(": ")
    game_id = _parse_game_id(game_id_str)
    reveals = _parse_reveals(reveals_str)
    return game_id, reveals


def part_one_solver(data):
    all_ids = set()
    invalid_ids = set()
    for line in data:
        game_id, reveals = parse_line(line)
        all_ids.add(game_id)
        for reveal in reveals:
            for color, number in reveal.items():
                if number > PART_ONE_CUBE_LIMITS[color]:
                    invalid_ids.add(game_id)
                    # could do a breaking thing here but meh -- fast enough
    return sum(all_ids - invalid_ids)


def test_part_one_solver():
    data = read_input("test_input.txt")
    assert part_one_solver(data) == 8


def part_two_solver(data):
    powers = dict()
    for line in data:
        game_id, reveals = parse_line(line)
        min_values = {}
        for reveal in reveals:
            for color, number in reveal.items():
                if min_values.get(color) is None or number > min_values[color]:
                    min_values[color] = number
        line_power = functools.reduce(operator.mul, min_values.values(), 1)
        powers[game_id] = line_power
    return sum(powers.values())


def test_part_two_solver():
    assert part_two_solver(read_input('test_input.txt')) == 2286


def read_input(input_file):
    with open(input_file) as f:
        return f.read().strip().split("\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("mode", type=int, default=1)
    return parser.parse_args()


MODE_MAP = {
    1: part_one_solver,
    2: part_two_solver,
}


def main():
    args = parse_args()
    data = read_input(args.input_file)
    func = MODE_MAP.get(args.mode)
    if not func:
        raise ValueError(f"Unknown mode: {args.mode}")
    print(func(data))


if __name__ == "__main__":
    main()
