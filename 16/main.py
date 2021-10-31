import argparse
import os
from typing import List

dna_map = {
    "A": "T",
    "C": "G",
    "G": "C",
    "T": "A"
}

codon_map = {
    "AAA": "K",
    "AAC": "N",
    "AAG": "K",
    "AAT": "N",
    "ACA": "T",
    "ACC": "T",
    "ACG": "T",
    "ACT": "T",
    "AGA": "R",
    "AGC": "S",
    "AGG": "R",
    "AGT": "S",
    "ATA": "I",
    "ATC": "I",
    "ATG": "M",
    "ATT": "I",
    "CAA": "Q",
    "CAC": "H",
    "CAG": "Q",
    "CAT": "H",
    "CCA": "P",
    "CCC": "P",
    "CCG": "P",
    "CCT": "P",
    "CGA": "R",
    "CGC": "R",
    "CGG": "R",
    "CGT": "R",
    "CTA": "L",
    "CTC": "L",
    "CTG": "L",
    "CTT": "L",
    "GAA": "E",
    "GAC": "D",
    "GAG": "E",
    "GAT": "D",
    "GCA": "A",
    "GCC": "A",
    "GCG": "A",
    "GCT": "A",
    "GGA": "G",
    "GGC": "G",
    "GGG": "G",
    "GGT": "G",
    "GTA": "V",
    "GTC": "V",
    "GTG": "V",
    "GTT": "V",
    "TAA": "X",
    "TAC": "Y",
    "TAG": "X",
    "TAT": "Y",
    "TCA": "S",
    "TCC": "S",
    "TCG": "S",
    "TCT": "S",
    "TGA": "X",
    "TGC": "C",
    "TGG": "W",
    "TGT": "C",
    "TTA": "L",
    "TTC": "F",
    "TTG": "L",
    "TTT": "F",
}


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


def __reverse_dna(dna: str) -> str:
    return "".join(reversed([dna_map[x] for x in dna]))


def __encode(dna: str, peptide: str, count = 3) -> List[str]:
    result_list = []
    for n in range(count):
        encoded = "".join(
            [
                codon_map[dna[i:i + count]]
                for i in range(n, int(len(dna) - n), count) 
                    if len(dna[i:i + count]) == count
            ]
        )

        result_list.extend(
            [
                dna[i * count + n:i * count + n + count * len(peptide)]
                for i in range(len(encoded) - len(peptide) + 1)
                    if encoded[i:i + len(peptide)] == peptide
            ]
        )
    return result_list


def calculate(input_path: str) -> str:
    with open(input_path, 'r') as file:
        data = file.readlines()
        dna = data[0].strip()
        peptide = data[1].strip()
        result_list = []
        result_list.extend(__encode(dna, peptide))
        result_list.extend([__reverse_dna(x) for x in __encode(__reverse_dna(dna), peptide)])
        return "\n".join(result_list)


def main(args=None) -> None:
    args=parse_args(args)
    assert os.path.exists(args.input), 'no input file'
    result = calculate(args.input)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    main()