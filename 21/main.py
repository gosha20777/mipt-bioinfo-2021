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
        n = int(file.readline())
        data = sorted(list(map(int, file.readline().split(','))))
        result = [i for i in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(len(data)):
                if i < data[j]:
                    break
                result[i] = result[i - data[j]] + 1
        return str(result[n])


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()