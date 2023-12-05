import argparse
from collections import namedtuple, defaultdict


TYPES = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]


def points_to(type_name):
    next_idx = TYPES.index(type_name) + 1
    if next_idx >= len(TYPES):
        return None
    return TYPES[next_idx]


def get_seeds(line) -> list[int]:
    assert line.startswith('seeds: ')
    start = line.index(':') + 2
    return [int(x) for x in line[start:].strip().split(' ')]


def test_get_seeds():
    assert get_seeds('seeds: 79 14 55 13') == [79, 14, 55, 13]


def get_numbers(line) -> tuple[int, int, int]:
    dest_start_str, src_start_str, length_str = line.strip().split(' ')
    return (int(dest_start_str), int(src_start_str), int(length_str))


def organize_data(data) -> dict[str, list[tuple[int, int, int]]]:
    """Given raw input lines of a file, return a dict of each section mapped to
    the values (list of 3-tuples) for that section.
    """
    organized_data = defaultdict(list)
    idx = 0
    mode = None

    while idx < len(data):
        line = data[idx]

        if line == '':  # skip blank lines
            continue

        # change mode if we're passing a "mode line"
        if not line[0].isnumeric() and any(line.startswith(t) for t in TYPES):
            mode = line[:line.index('-')].strip()

        # otherwise add the line to the current mode
        elif line[0].isnumeric():
            dest_start, src_start, length = get_numbers(line)
            organized_data[mode].append((dest_start, src_start, length))

        # next line
        idx += 1

    return organized_data


def find_next_id(source_id, data) -> int:
    """Follows a "node" along the path from seed to location.

    Given a source ID and a set of data -- one block from the input file, for
    example the seed-to-soil map (but not any other map) -- this function will
    return the destination ID contained within the map.

    Args:
        source_id:  The ID of the source thing, e.g. seeds
        data:  A list of 3-tuples from that category of inputs, e.g. the seed-to-soil map

    Returns:
        The ID of the destination thing, e.g. soil
    """
    for (dest_start, src_start, length) in data:
        if source_id >= src_start and source_id <= src_start + length:
            return dest_start + (source_id - src_start)
    return source_id  # per the instructions, default to same ID


def test_find_next_id():
    data = read_input('test_input.txt')
    data = organize_data(data[1:])
    assert find_next_id(98, data['seed']) == 50


def solution_one(data):
    seeds = get_seeds(data[0])
    organized_data = organize_data(data[1:])
    locations = []
    for seed in seeds:
        last_id = seed
        for i in range(0, len(TYPES)):
            this_type = TYPES[i]
            next_type = TYPES[i + 1] if i < len(TYPES) - 1 else None
            if next_type is not None:
                last_id = find_next_id(last_id, organized_data[this_type])
        locations.append(last_id)
    return min(locations)


def test_solution_one():
    assert solution_one(read_input('test_input.txt')) == 35


def solution_two(data):
    raise NotImplementedError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='input file')
    parser.add_argument('mode', type=int, help='output file')
    return parser.parse_args()


def read_input(input_file):
    data = None
    with open(input_file, 'r') as f:
        data = f.readlines()
    return [
        line.strip()
        for line in data
        if line.strip()
    ]


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
