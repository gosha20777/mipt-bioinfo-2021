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
        d += 1
        rows = dict()
        for row in file.readlines():
            row = ''.join(row.split())
            one, two = row.split('|')
            rows[(one[:n-1], two[:n-1])] = (one[1:n], two[1:n])
        while d > 0:
            temp_rows = dict()
            for k, v in rows.items():
                if v in rows.keys():
                    temp_k = tuple(k[i] + v[i][-1] for i in range(2))
                    temp_v = tuple(v[i] + rows[v][i][-1] for i in range(2))
                    temp_rows[temp_k] = temp_v
            d -= 1
            rows = temp_rows
        rows = {k[0] + k[1]: v[0] + v[1]
                 for k, v in rows.items()}
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