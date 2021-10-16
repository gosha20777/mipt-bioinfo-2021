import argparse
import os


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


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        n, d = list(map(int, file.readline().split()))
        rows = list(map(lambda x: x.replace("\n", "").split("|"), file.readlines())) 
        p1 = [x[0] for x in rows]
        p2 = [x[1] for x in rows]
        seq1 = "".join([x[0] for x in p1] + [p1[-1][1:]])
        seq2 = "".join([x[0] for x in p2] + [p2[-1][1:]])
        return seq1[:n+d] + seq2


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()