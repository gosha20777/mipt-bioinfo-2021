import argparse
import os
from typing import List

anins_map = {
    'G': 57,
    'A': 71,
    'S': 87,
    'P': 97,
    'V': 99,
    'T': 101,
    'C': 103,
    'I': 113,
    'N': 114,
    'D': 115,
    'K': 128,
    'E': 129,
    'M': 131,
    'H': 137,
    'F': 147,
    'R': 156,
    'Y': 163,
    'W': 186
}

mass_map = dict()


def parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Make submission')
    parser.add_argument(
        '-i', '--input',
        help='path to input file',
        type=str,
        required=True
    )
    parser.add_argument(
        '-o', '--output',
        help='path to output file',
        type=str,
        required=True
    )
    return parser.parse_args(args)


def __get_count_my_nass(mass: int):
    count = 0
    for k in anins_map.keys():
        if (mass - anins_map[k]) in mass_map.keys():
            count += mass_map[(mass - anins_map[k])]
        elif mass - anins_map[k] < 0:
            break
        elif mass - anins_map[k] == 0:
            count += 1
            return count
        elif mass - anins_map[k] > 0:
            count += __get_count_my_nass(mass - anins_map[k])
    mass_map[mass] = count
    return count


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        data = file.readlines()
        mass = tuple(map(int, data[0].split()))[0]
        result = __get_count_my_nass(mass)
        return f'{result}'


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()