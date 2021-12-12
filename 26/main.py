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

def __sort(p):
    res = []
    index_func = lambda perm, v: list(map(abs, perm)).index(v)
    sort_func = lambda perm, i, j: perm[:i] + list(map(lambda x: -x, perm[i:j + 1][::-1])) + perm[j + 1:]

    x = 0
    while x < len(p):
        if p[x] == x + 1:
            x += 1
        else:
            p = sort_func(
                p,
                x, index_func(p, x + 1))
            res.append(p)

    return res


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        data = file.readlines()[0]
        p = list(map(int, data[1:-1].replace("\n", "").split()))
        p = __sort(p)
        val_func = lambda value: ['-', '+'][value > 0] + str(abs(value))
        return "\n".join(
            ['(' + ' '.join([val_func(value) for value in perm]) + ')'
            for perm in p])
        

def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
