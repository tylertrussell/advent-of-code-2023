import argparse
from collections import namedtuple, defaultdict

Node = namedtuple('Node', ['type', 'value', 'next'])

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


def build_nodes(data) -> dict[str, dict[int, Node]]:
    nodes = defaultdict(dict)
    idx = 0
    mode = None

    while idx < len(data):
        line = data[idx]

        # change mode if we're passing a "mode line"
        if not line[0].isnumeric() and any(line.startswith(t) for t in TYPES):
            mode = line[:line.index('-')].strip()

        # otherwise add nodes
        elif line[0].isnumeric():
            dest_start, src_start, length = get_numbers(line)
            for i, _ in enumerate(range(src_start, src_start + length)):
                value = src_start + i
                new_node = Node(mode, value, dest_start + i)
                nodes[mode][value] = new_node

        # next line
        idx += 1

    return nodes


def get_node(node_type, node_id, all_nodes):
    node_type_dict = all_nodes[node_type]
    if node_id in node_type_dict:
        return node_type_dict[node_id]
    else:
        # items which are not mapped map to the next item of the same ID
        return Node(node_type, node_id, node_id)


def follow_nodes(node, all_nodes):
    next_type = points_to(node.type)
    if next_type:
        next_node = get_node(next_type, node.next, all_nodes)
        return follow_nodes(next_node, all_nodes)
    return node.value


def solution_one(data):
    seeds = get_seeds(data[0])
    nodes = build_nodes(data[1:])
    locations = []
    for seed in seeds:
        root = get_node('seed', seed, nodes)
        location = follow_nodes(root, nodes)
        locations.append(location)
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
