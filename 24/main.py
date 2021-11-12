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

def __add(x, i): 
    return x[:i] + '-' + x[i:]

def __load_blosum62():
    with open('matrix.txt') as file:
        data = [l.strip().split() for l in file.readlines()]
        return {
            (d[0], d[1]): int(d[2]) for d in data
        }


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        data = file.readlines()
        k = 5
        blosum62 = __load_blosum62()
        seq_1 = data[0].strip()
        seq_2 = data[1].strip()
        (h, w) = (len(seq_1) + 1, len(seq_2) + 1)
        fwd = np.zeros((h, w), dtype=np.int32)
        bwd = np.zeros((h, w), dtype=np.int32)
        for x in range(1, len(seq_1)+1):
            for y in range(1, len(seq_2)+1):
                l = [
                        fwd[x - 1, y] - k,
                        fwd[x, y - 1] - k,
                        fwd[x - 1, y - 1] + blosum62[seq_1[x - 1], 
                        seq_2[y - 1],
                        0
                    ]
                ]
                fwd[x, y] = max(l)
                bwd[x, y] = l.index(fwd[x, y])
        l = str(fwd.max())

        x_1, x_2 = np.unravel_index(fwd.argmax(), fwd.shape)
        seq_1, seq_2 = seq_1[:x_1], seq_2[:x_2]
        while bwd[x_1, x_2] != 3 and x_1 * x_2 != 0:
            if bwd[x_1, x_2] == 1:
                x_2 -= 1
                seq_1 = __add(seq_1, x_1)
            elif bwd[x_1, x_2] == 0:
                x_1 -= 1
                seq_2 = __add(seq_2, x_2)
            elif bwd[x_1, x_2] == 2:
                x_1 -= 1
                x_2 -= 1

        seq_1 = seq_1[x_1:]
        seq_2 = seq_2[x_2:]

        return "\n".join([l, seq_1, seq_2])


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()
