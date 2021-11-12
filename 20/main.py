import argparse
import os
from collections import defaultdict
import numpy as np

from hw19 import calculate as __calculate_leaderboard


def __get_spectrum_mass(s, m):
    spectrum = sorted(s)
    spectral_list = [
        spectrum[i] - spectrum[j]
            for i in range(len(spectrum))
            for j in range(i)
    ]
    spectral_list.extend(spectrum)
    spectral_list = list(filter(lambda x: 57 <= x <= 200, spectral_list))
    spectral_list_final = list(map(
            lambda x: (x, spectral_list.count(x)),
            set(spectral_list))
    )
    spectral_list_final = sorted(
        spectral_list_final, key=lambda x: x[1], reverse=True)
    t = spectral_list_final[m][1] if m < len(spectral_list_final) else -np.inf
    result = [x[0] for x in spectral_list_final if x[1] >= t]
    return result


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
        data = file.readlines()

        m = tuple(map(int, data[0].split()))[0]
        n = tuple(map(int, data[1].split()))[0]
        spectrum = list(map(int, data[2].split()))

        new_mass = __get_spectrum_mass(spectrum, m)
        result = __calculate_leaderboard(spectrum, n, new_mass)
        return "-".join(str(x) for x in result[0])


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()