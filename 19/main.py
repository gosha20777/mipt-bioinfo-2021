import argparse
import os
from collections import defaultdict
import numpy as np

mass_list = [
    57,
    71,
    87,
    97,
    99,
    101,
    103,
    113,
    114,
    115,
    128,
    129,
    131,
    137,
    147,
    156,
    163,
    186
]


def __get_weight(p_dct: dict, s_dct: dict) -> int:
    return sum([min(p_dct[i], s_dct[i]) for i in p_dct.keys()])


def __peptide2count_dict(peptide: list) -> dict:
    count_dict = defaultdict(int)
    for p in peptide:
        count_dict[p] += 1
    return count_dict


def __expand_mass_list(p_list: list, m_list: list) -> list:
    if len(p_list) == 0:
        return [[m] for m in m_list]
    return [p + [m] for p in p_list for m in m_list]


def __sub_peptide(peptide, position, length):
    if position + length <= len(peptide):
        return peptide[position: position+length]
    else:
        return peptide[position:] + peptide[:length + position - len(peptide)]


def __cyclo_peptide(peptide):
    return [__sub_peptide(peptide, pos, leng)
            for pos in range(len(peptide))
            for leng in range(1, len(peptide) + 1)]


def __cyclo_spectrum(pep):
    return sorted([sum(p) for p in __cyclo_peptide(pep)] + [0])


def __cut_leaderboard(leaderboard, spectrum_dct, k):
    weight_list = list(map(
        lambda x: (
            x, 
            __get_weight(
                __peptide2count_dict(
                    __cyclo_spectrum(x)
                ), 
                spectrum_dct
            )
        ),
        leaderboard))
    weight_list = sorted(
        weight_list, 
        key=lambda x: x[1], 
        reverse=True
    )
    t = weight_list[k][1] if k < len(weight_list) else -np.inf
    result = [x[0] for x in weight_list if x[1] >= t]
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

        n = tuple(map(int, data[0].split()))[0]
        ok = False
        top_list = []
        best_peptide = (0, 0)
        spectrum = tuple(map(int, data[1].split()))
        spectrum_dct = __peptide2count_dict(spectrum)
        

        while not ok:
            top_list = __expand_mass_list(top_list, mass_list)
            top_list = __cut_leaderboard(top_list, spectrum_dct, n)
            top_list = [p for p in top_list if sum(p) <= max(spectrum)]

            if len(top_list) == 0:
                ok = True
                break

            best_weight = __get_weight(__peptide2count_dict(__cyclo_spectrum(top_list[0])), spectrum_dct)
            if best_weight > best_peptide[1]:
                best_peptide = (top_list[0], best_weight)

        return "-".join(str(x) for x in best_peptide[0])


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()