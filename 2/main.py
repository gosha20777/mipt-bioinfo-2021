import argparse
import os

genome_dict = {
    "C": -1,
    "G": 1
}

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
        result_sum = 0

        def to_complex(x):
            nonlocal result_sum
            result_sum += genome_dict.get(x, 0)
            return result_sum

        result = list(map(lambda x: to_complex(x), genome))
        minimum = min(result)
        result = [str(i+1) for i, v in enumerate(result) if v == minimum]
        return "\t".join(result)


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()