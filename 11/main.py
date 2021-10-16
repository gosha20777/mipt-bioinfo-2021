import argparse
import os


def parse_args(args):
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
        rows = {row[:n-1]: row[1:n] for row in file.readlines()}
        while len(rows) != 1:
            temp_rows = dict()
            for k, v in rows.items():
                if v in rows.keys():
                    temp_rows[k + v[-1]] = v[0] + rows[v]
            rows = temp_rows
        k = list(rows.keys())[0]
        v = rows[k][-1]
        return f'{k}{v}'



def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()