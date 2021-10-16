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
        elements = set()
        seq = ['1' for _ in range(n)]
        elements.add('1' * n)
        pow = 2 ** n
        idx = 1

        while idx < pow:
            temp_seq = seq[-n+1:]
            if ''.join(temp_seq) + '0' in elements:
                seq.append('1')
                if ''.join(temp_seq) + '1' not in elements:
                    elements.add(''.join(temp_seq) + '1')
                    idx += 1
            else:
                seq.append('0')
                elements.add(''.join(temp_seq) + '0')
                idx += 1
        return ''.join(seq[:-n+1])


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()