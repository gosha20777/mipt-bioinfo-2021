import argparse
import os
from collections import defaultdict

anin_map = {
    'G': 57,
    'A': 71,
    'S': 87,
    'P': 97,
    'V': 99,
    'T': 101,
    'C': 103,
    'I': 113,
    'N': 114,
    'D': 115,
    'K': 128,
    'E': 129,
    'M': 131,
    'H': 137,
    'F': 147,
    'R': 156,
    'Y': 163,
    'W': 186
}

def __is_consistent(peptide: list, spectrum: list) -> bool:
    mass_list = [0 for _ in range(len(peptide) + 1)]
    for e in range(len(peptide)):
        mass_list[e + 1] = mass_list[e] + anin_map[peptide[e]]

    spectrum_mass_list = []
    for e in range(len(peptide)):
        for e2 in range(e + 1, len(peptide) + 1):
            spectrum_mass_list.append(mass_list[e2] - mass_list[e])
    spectrum_mass_list.append(0)
    spectrum_mass_list = sorted(spectrum_mass_list)

    for s in spectrum_mass_list:
        if spectrum_mass_list.count(s) > spectrum.count(s):
            return False
    return True


def __get_cyclo_spectrum(peptide: list, anins_map: dict) -> list:
    mass_list = [0 for _ in range(len(peptide) + 1)]
    for e in range(len(peptide)):
        mass_list[e + 1] = mass_list[e] + anins_map[peptide[e]]
    mass_list_len = mass_list[len(peptide)]
    
    result = []
    for e in range(len(peptide)):
        for e2 in range(e + 1, len(peptide) + 1):
            result.append(mass_list[e2] - mass_list[e])
            if e > 0 and e2 < len(peptide):
                result.append(mass_list_len - (mass_list[e2] - mass_list[e]))
    result.append(0)
    return sorted(result)


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
        data = file.readlines()[0].split()
        
        spectrum = [int(d) for d in data]
        cand_peptide_list = ['']
        result_peptide_list = []

        while cand_peptide_list:
            new_peptide_list = []
            for p in cand_peptide_list:
                for a in anin_map:
                    new_peptide_list.append(p + a)
            cand_peptide_list = new_peptide_list
            min_list = []
            
            for p in range(len(cand_peptide_list)):
                peptide = cand_peptide_list[p]

                peptide_mass = 0
                for e in range(len(peptide)):
                    peptide_mass += anin_map[peptide[e]]

                if peptide_mass == max(spectrum):
                    if __get_cyclo_spectrum(peptide, anin_map) == spectrum:
                        result_peptide_list.append(peptide)
                        min_list.append(peptide)

                elif not __is_consistent(peptide, spectrum):
                    min_list.append(peptide)

            for i in range(len(min_list)):
                cand_peptide_list.remove(min_list[i])

        finel_peptide_list = []
        for peptide in result_peptide_list:
            mass_peptide_list = []
            for i in range(len(peptide)):
                mass_peptide_list.append(anin_map[peptide[i]])
            finel_peptide_list.append('-'.join(str(i) for i in mass_peptide_list))
        result = ' '.join(str(i) for i in finel_peptide_list)
        return result


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()