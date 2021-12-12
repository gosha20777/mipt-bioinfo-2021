import argparse
import os
from numpy.random import randint


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


def get_hamming_distance(first, second):
    result = 0
    for a, b in zip(first, second):
        if a != b:
            result += 1
    return result


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        pattern = file.readline()[:-1]
        dna_list = file.readline().split()
        k = len(pattern)
        result = 0
        for dna in dna_list:
            h_d = 2 ** 30
            for begin in range(len(dna) - k + 1):
                new_h_d = get_hamming_distance(
                    pattern, 
                    dna[begin:begin+k]
                )
                if h_d > new_h_d:
                    h_d = new_h_d
            result += h_d
        return str(result)


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
