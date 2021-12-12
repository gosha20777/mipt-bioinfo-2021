import argparse
import os
import numpy as np


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

def __breakpoint(p):
    return sum(
        map(lambda x, y: x - y != 1, p + [len(p) + 1], [0] + p)
    )


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        data = file.readlines()[0]
        p = list(map(int, data[1:-1].replace("\n", "").replace("+", "").split()))
        return str(__breakpoint(p))
        

def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
