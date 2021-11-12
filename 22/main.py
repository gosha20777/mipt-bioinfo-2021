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
        line = file.readline().split()
        n, m = int(line[0]), int(line[1])
        down_matrix = [list(map(int, file.readline().split())) for _ in range(n)]
        file.readline()
        right_matrix = [list(map(int, file.readline().split())) for _ in range(n + 1)]

        result = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
        for i in range(1, n + 1):
            result[i][0] = result[i - 1][0] + down_matrix[i - 1][0]
        for i in range(1, m + 1):
            result[0][i] = result[0][i - 1] + right_matrix[0][i - 1]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                result[i][j] = max(
                    result[i - 1][j] + down_matrix[i - 1][j], 
                    result[i][j - 1] + right_matrix[i][j - 1]
                )
        return str(result[n][m])


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
