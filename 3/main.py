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
        pattern = file.readline()[:-1]
        text = file.readline()[:-1]
        d = int(file.readline())
        result = []
        n = len(pattern)
        for i in range(len(text) - n):
            delta = sum([x != y for x, y in zip(pattern, text[i:i+n])])
            if delta <= d:
                result.append(str(i))
        return "\t".join(result)


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()