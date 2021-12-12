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
        genome = file.readline()
        k, L, t = list(map(int, file.readline().split()))
        result = set()
        for begin in range(len(genome) - L + 1):
            if genome.count(genome[begin : begin + k], begin, begin + L) >= t:
                result.add(genome[begin : begin + k])
        return "\t".join(list(result))


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()